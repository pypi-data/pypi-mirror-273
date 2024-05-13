# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
Batch-related commands
"""

import os
import datetime
import logging
import sys

from rattail.commands import Subcommand, date_argument, dict_argument
from rattail.progress import SocketProgress
from rattail.util import simple_error


log = logging.getLogger(__name__)


class BatchHandlerCommand(Subcommand):
    """
    Base class for commands which invoke a batch handler.

    Note that if such a command fails to run its action, the error
    will be written to STDOUT as a simple message string.  If the full
    traceback is needed, logs must be consulted.  This is done for
    sake of letting the caller capture output for display to the user
    when something goes wrong.
    """

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--batch-type', metavar='KEY',
                            help="Type of batch to be dealt with, e.g. 'vendor_catalog'")
        parser.add_argument('--dry-run', action='store_true',
                            help="Go through the full motions and allow logging etc. to "
                            "occur, but rollback (abort) the transaction at the end.")

    def get_handler(self, args):
        """
        Must return the batch handler to use, per the given ``args``
        object.

        Default logic assumes that ``args`` has a ``batch_type``
        attribute, which determines which batch handler should be
        used.  That is figured out by calling
        :meth:`~rattail.app.AppHandler.get_batch_handler()` on the app
        handler.

        :param args: Reference to the
           :class:`python:argparse.Namespace` instance, which was the
           result of parsing the command line args.

        :returns: Must return the batch handler.  This will be an
           instance of some class which derives from
           :class:`~rattail.batch.handlers.BatchHandler`.
        """
        return self.app.get_batch_handler(args.batch_type)

    def run(self, args):
        handler = self.get_handler(args)
        session = self.make_session()
        user = self.get_runas_user(session)

        try:
            success = self.do_stuff(args, handler, session, user)
        except Exception as error:
            log.warning("handler action failed", exc_info=True)
            # nb. only write "simple" error string to stdout, in case
            # caller (e.g. web app) is capturing that for display to
            # user.  admin can consult logs if more info is needed.
            # we do *not* write to stderr, because logging probably
            # is already doing that; we want to avoid mixing them.
            # TODO: this admittedly seems brittle, maybe caller should
            # pass command line flags to control this?
            self.stdout.write(simple_error(error))
            session.rollback()
            session.close()
            sys.exit(42)

        self.finalize_session(session, dry_run=args.dry_run,
                              success=success)

    def do_stuff(self, args, handler, session, user):
        raise NotImplementedError


class MakeBatch(BatchHandlerCommand):
    """
    Make a new batch, from a data file
    """
    name = 'make-batch'
    description = __doc__.strip()

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--input-file', metavar='PATH', required=True,
                            help="Path to single input file, to be used as data "
                            "source for the new batch.  (File format will vary "
                            "depending on batch type.)")

        parser.add_argument('--kwargs', type=dict_argument, default={},
                            help="Optional JSON-encoded string containing extra "
                            "keyword arguments to be passed to the handler's batch "
                            "creation logic.")

    def do_stuff(self, args, handler, session, user):
        """
        This will create a new batch of the specified type, then populate it
        with the given data file.
        """
        if not os.path.exists(args.input_file):
            raise RuntimeError("input file path does not exist: {}".format(args.input_file))

        kwargs = dict(args.kwargs)
        delete_if_empty = kwargs.pop('delete_if_empty', False)
        auto_execute_allowed = kwargs.pop('auto_execute_allowed', True)

        batch = handler.make_batch(session, created_by=user, **kwargs)
        handler.set_input_file(batch, args.input_file)
        handler.do_populate(batch, user)

        if delete_if_empty:
            session.flush()
            if not batch.data_rows:
                log.debug("auto-deleting empty '%s' batch: %s", handler.batch_key, batch)
                handler.do_delete(batch, dry_run=args.dry_run,
                                  progress=self.progress)
                batch = None

        if batch and auto_execute_allowed and handler.auto_executable(batch):
            handler.execute(batch, user=user)
            batch.executed = self.app.make_utc()
            batch.executed_by = user

        return True


class BatchAction(BatchHandlerCommand):
    """
    Base class for commands which invoke a handler to act on a single batch.
    """

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('batch_uuid',
                            help="UUID of the batch to be populated.")

    def do_stuff(self, args, handler, session, user):
        """
        This will invoke some action on the batch.
        """
        batch = session.get(handler.batch_model_class, args.batch_uuid)
        if not batch:
            raise RuntimeError("Batch of type '{}' not found: {}".format(args.batch_type, args.batch_uuid))

        return self.action(args, handler, batch, user)


class AutoReceiveBatch(BatchAction):
    """
    Auto-receive all items in a receiving batch
    """
    name = 'auto-receive'
    description = __doc__.strip()

    def action(self, args, handler, batch, user):
        return handler.auto_receive_all_items(batch, progress=self.progress)


class PopulateBatch(BatchAction):
    """
    Populate initial data for a batch
    """
    name = 'populate-batch'
    description = __doc__.strip()

    def action(self, args, handler, batch, user):
        return handler.do_populate(batch, user, progress=self.progress)


class RefreshBatch(BatchAction):
    """
    Refresh data for a batch
    """
    name = 'refresh-batch'
    description = __doc__.strip()

    def action(self, args, handler, batch, user):
        return handler.do_refresh(batch, user, progress=self.progress)


class ExecuteBatch(BatchAction):
    """
    Execute a batch
    """
    name = 'execute-batch'
    description = __doc__.strip()

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--kwargs', type=dict_argument, default={},
                            help="Optional JSON-encoded string containing extra "
                            "keyword arguments to be passed to the handler's batch "
                            "execution function.")

    def action(self, args, handler, batch, user):
        return handler.do_execute(batch, user, progress=self.progress, **args.kwargs)


class PurgeBatches(BatchHandlerCommand):
    """
    Purge old batches from the database
    """
    name = 'purge-batches'
    description = __doc__.strip()

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--before', type=date_argument, metavar='DATE',
                            help="Purge all batches executed prior to this date.  If not "
                            "specified, will use --before-days to calculate instead.")

        parser.add_argument('--before-days', type=int, default=90, metavar='DAYS',
                            help="Number of days before the current date, to be used "
                            "as the cutoff date if --before is not specified.  Default "
                            "is 90 days before current date.")

        parser.add_argument('--list-types', action='store_true',
                            help="If set, list available batch types instead of trying "
                            "to purge anything.")


    def run(self, args):
        if args.list_types:
            self.list_types()
            return

        handler = self.get_handler(args)
        session = self.make_session()

        kwargs = {
            'dry_run': args.dry_run,
            'progress': self.progress,
        }
        if args.before:
            before = datetime.datetime.combine(args.before, datetime.time(0))
            before = self.app.localtime(before)
            kwargs['before'] = before
        else:
            kwargs['before_days'] = args.before_days

        purged = handler.purge_batches(session, **kwargs)

        if args.dry_run:
            session.rollback()
            log.info("dry run, so transaction was rolled back")
        else:
            session.commit()
            log.info("transaction was committed")
        session.close()

    def list_types(self):
        from rattail.batch.handlers import get_batch_types

        keys = get_batch_types(self.config)
        for key in keys:
            self.stdout.write("{}\n".format(key))
