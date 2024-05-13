# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2024 Lance Edgar
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
Console Commands - base classes and core commands
"""

import importlib
import os
import sys
import json
import platform
import argparse
import datetime
import socket
import shutil
import subprocess
import warnings
import logging
from getpass import getpass

import humanize

from wuttjamaican.cmd.base import (Command as WuttaCommand,
                                   CommandArgumentParser,
                                   Subcommand as WuttaSubcommand)
from wuttjamaican.util import parse_list

from rattail import __version__
from rattail.progress import ConsoleProgress, SocketProgress
from rattail.config import make_config
from rattail.util import progress_loop
from rattail.db.config import configure_versioning


log = logging.getLogger(__name__)


class ArgumentParser(CommandArgumentParser):
    """
    Custom argument parser.

    This is a compatibility wrapper around upstream
    :class:`wuttjamaican:wuttjamaican.commands.base.CommandArgumentParser`.
    New code should use that instead; this will eventually be removed.
    """

    def __init__(self, *args, **kwargs):
        warnings.warn("the custom ArgumentParser in rattail is deprecated; "
                      "please use the one from wuttjamaican instead",
                      DeprecationWarning, stacklevel=2)
        super().__init__(*args, **kwargs)


def date_argument(string):
    """
    Validate and coerce a date argument.

    This function is designed be used as the ``type`` parameter when calling
    ``ArgumentParser.add_argument()``, e.g.::

       parser = ArgumentParser()
       parser.add_argument('--date', type=date_argument)
    """
    try:
        date = datetime.datetime.strptime(string, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError("Date must be in YYYY-MM-DD format")
    return date


def dict_argument(string):
    """
    Coerce the given string to a Python dictionary.  The string is assumed to
    be JSON-encoded; this function merely invokes ``json.loads()`` on it.

    This function is designed be used as the ``type`` parameter when calling
    ``ArgumentParser.add_argument()``, e.g.::

       parser = ArgumentParser()
       parser.add_argument('--date', type=dict_argument)
    """
    try:
        return json.loads(string)
    except json.decoder.JSONDecodeError:
        raise argparse.ArgumentTypeError("Argument must be valid JSON-encoded string")


def list_argument(string):
    """
    Coerce the given string to a list of strings, splitting on whitespace
    and/or commas.

    This function is designed be used as the ``type`` parameter when calling
    ``ArgumentParser.add_argument()``, e.g.::

       parser = ArgumentParser()
       parser.add_argument('--things', type=list_argument)
    """
    return parse_list(string)


class RattailCommand(WuttaCommand):
    """
    The primary command for Rattail.

    This inherits from
    :class:`wuttjamaican:wuttjamaican.commands.base.Command` so see
    those docs for more info.

    Custom apps based on Rattail will probably want to make and
    register their own ``Command`` class derived from this one.  Again
    see upstream docs for more details.

    Rattail extends the upstream class by adding the following:
    """
    name = 'rattail'
    version = __version__
    description = "Rattail Software Framework"

    @property
    def db_config_section(self):
        """
        Name of section in config file which should have database connection
        info.  This defaults to ``'rattail.db'`` but may be overridden so the
        command framework can sit in front of a non-Rattail database if needed.

        This is used to auto-configure a "default" database engine for the app,
        when any command is invoked.
        """
        # TODO: surely this can be more dynamic? or is it really being used?
        return 'rattail.db'

    @property
    def db_session_factory(self):
        """
        Returns a reference to the configured session factory.

        This is a compatibility wrapper around
        :meth:`rattail.app.AppHandler.make_session()`.  New code
        should use that instead; this may eventually be removed.
        """
        return self.config.get_app().make_session

    @property
    def db_model(self):
        """
        Returns a reference to configured model module.

        This is a compatibility wrapper around
        :meth:`rattail.config.RattailConfig.get_model()`.  New
        code should use that instead; this may eventually be removed.
        """
        return self.config.get_model()

    def iter_subcommands(self):
        """
        Returns a generator for the subcommands, sorted by name.

        This should probably not be used; instead see upstream
        :meth:`wuttjamaican:wuttjamaican.commands.base.Command.sorted_subcommands()`.
        """
        for subcmd in self.sorted_subcommands():
            yield subcmd

    def add_args(self):
        """
        Configure args for the main command arg parser.

        Rattail extends the upstream
        :meth:`~wuttjamaican:wuttjamaican.commands.base.Command.add_args()`
        by adding various command line args which have traditionally
        been available for it.  Some of these may disappear some day
        but no changes are planned just yet.
        """
        super().add_args()
        parser = self.parser

        # TODO: i think these aren't really being used in practice..?
        parser.add_argument('-n', '--no-init', action='store_true', default=False)
        parser.add_argument('--no-extend-config', dest='extend_config', action='store_false')

        parser.add_argument('--verbose', action='store_true')
        parser.add_argument('--progress-socket',
                            help="Optional socket (e.g. localhost:8487) to which progress info should be written.")
        parser.add_argument('--runas', '-R', metavar='USERNAME',
                            help="Optional username to impersonate when running the command.  "
                            "This is only relevant for / used by certain commands.")

        # data versioning
        parser.add_argument('--versioning', action='store_true',
                            help="Force *enable* of data versioning.  If set, then --no-versioning "
                            "cannot also be set.  If neither is set, config will determine whether "
                            "or not data versioning should be enabled.")
        parser.add_argument('--no-versioning', action='store_true',
                            help="Force *disable* of data versioning.  If set, then --versioning "
                            "cannot also be set.  If neither is set, config will determine whether "
                            "or not data versioning should be enabled.")

    def make_config(self, args):
        """
        Make the config object in preparation for running a subcommand.

        See also upstream
        :meth:`~wuttjamaican:wuttjamaican.commands.base.Command.make_config()`
        but for now, Rattail overrides this completely, mostly for the
        sake of versioning setup.
        """
        # TODO: can we make better args so this is handled by argparse somehow?
        if args.versioning and args.no_versioning:
            self.stderr.write("Cannot pass both --versioning and --no-versioning\n")
            sys.exit(1)

        # if args say not to "init" then we make a sort of empty config
        if args.no_init:
            config = make_config([], extend=False, versioning=False)

        else: # otherwise we make a proper config, and maybe turn on versioning
            logging.basicConfig()
            config = make_config(args.config_paths, plus_files=args.plus_config_paths,
                                 extend=args.extend_config, versioning=False)
            if args.versioning:
                configure_versioning(config, force=True)
            elif not args.no_versioning:
                configure_versioning(config)

        # import our primary data model now, just in case it hasn't fully been
        # imported yet.  this it to be sure association proxies and the like
        # are fully wired up in the case of extensions
        # TODO: what about web apps etc.? i guess i was only having the problem
        # for some importers, e.g. basic CORE API -> Rattail w/ the schema
        # extensions in place from rattail-corepos
        try:
            config.get_model()
        except ImportError:
            pass

        return config

    def prep_subcommand(self, subcmd, args):
        """
        Rattail overrides this method to apply some of the global args
        directly to the subcommand object.

        See also upstream
        :meth:`~wuttjamaican:wuttjamaican.commands.base.Command.prep_subcommand()`.
        """
        # figure out if/how subcommand should show progress
        subcmd.show_progress = args.progress
        subcmd.progress = None
        if subcmd.show_progress:
            if args.progress_socket:
                host, port = args.progress_socket.split(':')
                subcmd.progress = SocketProgress(host, int(port))
            else:
                subcmd.progress = ConsoleProgress

        # maybe should be verbose
        subcmd.verbose = args.verbose

        # TODO: make this default to something from config?
        subcmd.runas_username = args.runas or None


# TODO: deprecate / remove this?
Command = RattailCommand


class RattailSubcommand(WuttaSubcommand):
    """
    Base class for subcommands.

    This inherits from :class:`wuttjamaican.commands.base.Subcommand`
    so see those docs for more info.

    Rattail extends the subcommand to include:

    .. attribute:: runas_username

       Username (:attr:`~rattail.db.model.users.User.username`)
       corresponding to the :class:`~rattail.db.model.users.User`
       which the command should "run as" - i.e.  for sake of version
       history etc.

    .. attribute:: show_progress

       Boolean indicating whether progress should be shown for the
       subcommand.

    .. attribute:: progress

       Optional factory to be used when creating progress objects.
       This is ``None`` by default but if :attr:`show_progress` is
       enabled, then :class:`~rattail.progress.ConsoleProgress` is the
       default factory.

    .. attribute:: verbose

       Flag indicating the subcommand should be free to print
       arbitrary messages to
       :attr:`~wuttjamaican:wuttjamaican.commands.base.Subcommand.stdout`.
    """
    runas_username = None
    show_progress = False
    progress = None
    verbose = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # TODO: deprecate / remove this
        self.parent = self.command

    def add_args(self):
        """
        This is the "same" as upstream
        :meth:`wuttjamaican:wuttjamaican.commands.base.Subcommand.add_args()`
        except Rattail must customize this to also invoke its
        deprecated method, :meth:`add_parser_args()`.
        """
        super().add_args()
        self.add_parser_args(self.parser)

    def add_parser_args(self, parser):
        """
        This method is deprecated and will eventually be removed;
        please define :meth:`add_args()` instead.
        """

    @property
    def model(self):
        return self.parent.db_model

    def make_session(self):
        session = self.parent.db_session_factory()
        user = self.get_runas_user(session=session)
        if user:
            session.set_continuum_user(user)
        return session

    def finalize_session(self, session, dry_run=False, success=True):
        """
        Wrap up the given session, per the given arguments.  This is meant to
        provide a simple convenience, for commands which must do work within a
        DB session, but would like to support a "dry run" mode.
        """
        if dry_run:
            session.rollback()
            log.info("dry run, so transaction was aborted")
        elif success:
            session.commit()
            log.info("transaction was committed")
        else:
            session.rollback()
            log.warning("action failed, so transaction was rolled back")
        session.close()

    def get_runas_user(self, session=None, username=None):
        """
        Returns a proper :class:`~rattail.db.model.users.User` object
        which the app should "run as" - which would then be used to
        assign authorship to certain actions taken, for versioning and
        batch execution etc.

        This will attempt to locate the given user record in the DB,
        querying as needed.

        :param session: Optional DB session for the lookup.  If not
           specified, one may be created automatically.

        :param username: Optional username.  If not specified, the
           subcommand (current instance) may provide a default
           username via its :attr:`runas_username` attribute, or else
           config will be checked for a default.  If no default
           username can be found, then no DB lookup will be done and
           the method simply returns ``None``.

        :returns: The ``User`` object, or ``None``.

        To define the default user via config, add something like:

        .. code-block:: ini

           [rattail]
           runas.default = myuser
        """
        from sqlalchemy import orm

        if username is None:
            if hasattr(self, 'runas_username'):
                username = self.runas_username
            if not username and self.config:
                username = self.config.get('rattail', 'runas.default')
        if username:
            user = None
            with self.app.short_session(session=session) as s:
                try:
                    user = s.query(self.model.User).filter_by(username=username).one()
                except orm.exc.NoResultFound:
                    pass
                else:
                    if not session:
                        s.expunge(user)
            return user

    def progress_loop(self, func, items, factory=None, **kwargs):
        return progress_loop(func, items, factory or self.progress, **kwargs)

    def get_pip_path(self):
        return os.path.join(sys.prefix, 'bin', 'pip')

    def require_prompt_toolkit(self):
        try:
            import prompt_toolkit
        except ImportError:
            value = input("\nprompt_toolkit is not installed.  shall i install it? [Yn] ")
            value = value.strip()
            if value and not self.config.parse_bool(value):
                self.stderr.write("prompt_toolkit is required; aborting\n")
                sys.exit(1)

            pip = self.get_pip_path()
            subprocess.check_call([pip, 'install', 'prompt_toolkit'])

    def require_rich(self):
        try:
            import rich
        except ImportError:
            value = input("\nrich is not installed.  shall i install it? [Yn] ")
            value = value.strip()
            if value and not self.config.parse_bool(value):
                self.stderr.write("rich is required; aborting\n")
                sys.exit(1)

            pip = self.get_pip_path()
            subprocess.check_call([pip, 'install', 'rich'])

    def rprint(self, *args, **kwargs):
        self.require_rich()

        # TODO: this could look different once python2 is out of the
        # picture; but must avoid `print` keyword for python2
        import rich
        rprint = getattr(rich, 'print')
        return rprint(*args, **kwargs)

    def basic_prompt(self, info, default=None, is_password=False, is_bool=False,
                     required=False):
        self.require_prompt_toolkit()

        from prompt_toolkit import prompt
        from prompt_toolkit.styles import Style

        # message formatting styles
        style = Style.from_dict({
            '': '',
            'bold': 'bold',
        })

        # build prompt message
        message = [
            ('', '\n'),
            ('class:bold', info),
        ]
        if default is not None:
            if is_bool:
                message.append(('', ' [{}]: '.format('Y' if default else 'N')))
            else:
                message.append(('', ' [{}]: '.format(default)))
        else:
            message.append(('', ': '))

        # prompt user for input
        try:
            text = prompt(message, style=style, is_password=is_password)
        except (KeyboardInterrupt, EOFError):
            self.rprint("\n\t[bold yellow]operation canceled by user[/bold yellow]\n",
                        file=self.stderr)
            sys.exit(2)

        if is_bool:
            if text == '':
                return default
            elif text.upper() == 'Y':
                return True
            elif text.upper() == 'N':
                return False
            self.rprint("\n\t[bold yellow]ambiguous, please try again[/bold yellow]\n")
            return self.basic_prompt(info, default, is_bool=True)

        if required and not text and not default:
            return self.basic_prompt(info, default, is_password=is_password,
                                     required=True)

        return text or default


# TODO: deprecate / remove this?
Subcommand = RattailSubcommand


class CheckDatabase(Subcommand):
    """
    Do basic sanity checks on a Rattail DB
    """
    name = 'checkdb'
    description = __doc__.strip()

    def run(self, args):
        import sqlalchemy as sa

        try:
            with self.config.rattail_engine.begin() as cxn:
                cxn.execute(sa.text("select version()"))
        except sa.exc.OperationalError as e:
            self.stderr.write("\nfailed to connect to DB!\n\n{}\n".format(e))
            sys.exit(1)

        self.stdout.write("All checks passed.\n")


class CloneDatabase(Subcommand):
    """
    Clone (supported) data from a source DB to a target DB
    """
    name = 'clonedb'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('source_engine',
                            help="SQLAlchemy engine URL for the source database.")
        parser.add_argument('target_engine',
                            help="SQLAlchemy engine URL for the target database.")
        parser.add_argument('-m', '--model', default='rattail.db.model',
                            help="Dotted path of Python module which contains the data model.")
        parser.add_argument('-C', '--classes', nargs='*',
                            help="Model classes which should be cloned.  Possible values here "
                            "depends on which module contains the data model.  If no classes "
                            "are specified, all available will be cloned.")

    def run(self, args):
        from sqlalchemy import create_engine, orm

        model = importlib.import_module(args.model)
        classes = args.classes
        assert classes

        source_engine = create_engine(args.source_engine)
        target_engine = create_engine(args.target_engine)
        model.Base.metadata.drop_all(bind=target_engine)
        model.Base.metadata.create_all(bind=target_engine)

        Session = orm.sessionmaker()
        src_session = Session(bind=source_engine)
        dst_session = Session(bind=target_engine)

        for clsname in classes:
            log.info("cloning data for model: %s", clsname)
            cls = getattr(model, clsname)
            src_query = src_session.query(cls)
            count = src_query.count()
            log.debug("found %d %s records to clone", count, clsname)
            if not count:
                continue

            mapper = orm.class_mapper(cls)
            key_query = src_session.query(*mapper.primary_key)

            prog = None
            if self.progress:
                prog = self.progress("Cloning data for model: {0}".format(clsname), count)
            for i, key in enumerate(key_query, 1):

                src_instance = src_query.get(key)
                dst_session.merge(src_instance)
                dst_session.flush()

                if prog:
                    prog.update(i)
            if prog:
                prog.destroy()

        src_session.close()
        dst_session.commit()
        dst_session.close()


class EmailBouncer(Subcommand):
    """
    Interacts with the email bouncer daemon.  This command expects a
    subcommand; one of the following:

    * ``rattail bouncer start``
    * ``rattail bouncer stop``
    """
    name = 'bouncer'
    description = "Manage the email bouncer daemon"

    def add_parser_args(self, parser):
        subparsers = parser.add_subparsers(title='subcommands')

        start = subparsers.add_parser('start', help="Start service")
        start.set_defaults(subcommand='start')
        stop = subparsers.add_parser('stop', help="Stop service")
        stop.set_defaults(subcommand='stop')

        parser.add_argument('-p', '--pidfile', metavar='PATH', default='/var/run/rattail/bouncer.pid',
                            help="Path to PID file.")
        parser.add_argument('--daemonize', action='store_true',
                            help="DEPRECATED")
        parser.add_argument('--no-daemonize',
                            '-D', '--do-not-daemonize',
                            action='store_false', dest='daemonize',
                            help="DEPRECATED")

    def run(self, args):
        from rattail.bouncer.daemon import BouncerDaemon

        daemon = BouncerDaemon(args.pidfile, config=self.config)
        if args.subcommand == 'stop':
            daemon.stop()
        else: # start
            try:
                daemon.start(daemonize=False)
            except KeyboardInterrupt:
                self.stderr.write("Interrupted.\n")


class FileMonitorCommand(Subcommand):
    """
    Interacts with the file monitor service; called as ``rattail filemon``.
    This command expects a subcommand; one of the following:

    * ``rattail filemon start``
    * ``rattail filemon stop``

    On Windows platforms, the following additional subcommands are available:

    * ``rattail filemon install``
    * ``rattail filemon uninstall`` (or ``rattail filemon remove``)

    .. note::
       The Windows Vista family of operating systems requires you to launch
       ``cmd.exe`` as an Administrator in order to have sufficient rights to
       run the above commands.

    .. See :doc:`howto.use_filemon` for more information.
    """

    name = 'filemon'
    description = "Manage the file monitor daemon"

    def add_parser_args(self, parser):
        subparsers = parser.add_subparsers(title='subcommands')

        start = subparsers.add_parser('start', help="Start service")
        start.set_defaults(subcommand='start')
        stop = subparsers.add_parser('stop', help="Stop service")
        stop.set_defaults(subcommand='stop')

        if sys.platform in ('linux', 'linux2'):
            parser.add_argument('-p', '--pidfile',
                                help="Path to PID file.", metavar='PATH')
            parser.add_argument('--daemonize', action='store_true',
                                help="DEPRECATED")
            parser.add_argument('--no-daemonize',
                                '-D', '--do-not-daemonize',
                                action='store_false', dest='daemonize',
                                help="DEPRECATED")

        elif sys.platform == 'win32': # pragma no cover

            install = subparsers.add_parser('install', help="Install service")
            install.set_defaults(subcommand='install')
            install.add_argument('-a', '--auto-start', action='store_true',
                                 help="Configure service to start automatically.")
            install.add_argument('-U', '--username',
                                 help="User account under which the service should run.")

            remove = subparsers.add_parser('remove', help="Uninstall (remove) service")
            remove.set_defaults(subcommand='remove')

            uninstall = subparsers.add_parser('uninstall', help="Uninstall (remove) service")
            uninstall.set_defaults(subcommand='remove')

            debug = subparsers.add_parser('debug', help="Run service in debug mode")
            debug.set_defaults(subcommand='debug')

    def run(self, args):
        if sys.platform in ('linux', 'linux2'):
            from rattail.filemon import linux as filemon

            if args.subcommand == 'start':
                filemon.start_daemon(self.config, args.pidfile)

            elif args.subcommand == 'stop':
                filemon.stop_daemon(self.config, args.pidfile)

        elif sys.platform == 'win32': # pragma no cover
            self.run_win32(args)

        else:
            self.stderr.write("File monitor is not supported on platform: {0}\n".format(sys.platform))
            sys.exit(1)

    def run_win32(self, args): # pragma no cover
        from rattail.win32 import require_elevation
        from rattail.win32 import service
        from rattail.win32 import users
        from rattail.filemon import win32 as filemon

        require_elevation()

        options = []
        if args.subcommand == 'install':

            username = args.username
            if username:
                if '\\' in username:
                    server, username = username.split('\\')
                else:
                    server = socket.gethostname()
                if not users.user_exists(username, server):
                    sys.stderr.write("User does not exist: {0}\\{1}\n".format(server, username))
                    sys.exit(1)

                password = ''
                while password == '':
                    password = getpass(str("Password for service user: ")).strip()
                options.extend(['--username', r'{0}\{1}'.format(server, username)])
                options.extend(['--password', password])

            if args.auto_start:
                options.extend(['--startup', 'auto'])

        service.execute_service_command(filemon, args.subcommand, *options)

        # If installing with custom user, grant "logon as service" right.
        if args.subcommand == 'install' and args.username:
            users.allow_logon_as_service(username)

        # TODO: Figure out if the following is even required, or if instead we
        # should just be passing '--startup delayed' to begin with?

        # If installing auto-start service on Windows 7, we should update
        # its startup type to be "Automatic (Delayed Start)".
        # TODO: Improve this check to include Vista?
        if args.subcommand == 'install' and args.auto_start:
            if platform.release() == '7':
                name = filemon.RattailFileMonitor._svc_name_
                service.delayed_auto_start_service(name)


class MailMonitorCommand(Subcommand):
    """
    Interacts with the mail monitor service; called as ``rattail
    mailmon``.  This command expects a subcommand; one of the
    following:

    * ``rattail mailmon start``
    * ``rattail mailmon stop``
    """
    name = 'mailmon'
    description = "Manage the mail monitor daemon"

    def add_parser_args(self, parser):
        subparsers = parser.add_subparsers(title='subcommands')

        start = subparsers.add_parser('start', help="Start service")
        start.set_defaults(subcommand='start')

        stop = subparsers.add_parser('stop', help="Stop service")
        stop.set_defaults(subcommand='stop')

        parser.add_argument('-p', '--pidfile', metavar='PATH', default='/var/run/rattail/mailmon.pid',
                            help="Path to PID file.")

    def run(self, args):
        from rattail.mailmon.daemon import MailMonitorDaemon

        daemon = MailMonitorDaemon(args.pidfile, config=self.config)
        if args.subcommand == 'stop':
            daemon.stop()
        else: # start
            try:
                daemon.start(daemonize=False)
            except KeyboardInterrupt:
                self.stderr.write("Interrupted.\n")


class MakeConfig(Subcommand):
    """
    Generate stub config file(s) where you want them
    """
    name = 'make-config'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('-T', '--type', metavar='NAME', default='rattail',
                            help="Type of config file to create; defaults to 'rattail' "
                            "which will generate 'rattail.conf'")
        parser.add_argument('-O', '--output', metavar='PATH', default='.',
                            help="Path where the config file is to be generated.  This can "
                            "be the full path including filename, or just the folder, in which "
                            "case the filename is inferred from 'type'.  Default is to current "
                            "working folder.")
        parser.add_argument('--list-types', '-l', action='store_true',
                            help="List the types of config files this tool can "
                            "generate.")

    def run(self, args):
        if args.list_types:
            self.list_types()
            return

        template_path = self.app.find_config_template(args.type)
        if not template_path:
            self.stderr.write("config template not found for type: {}\n".format(args.type))
            sys.exit(1)

        output_path = os.path.abspath(args.output)
        if os.path.isdir(output_path):
            output_path = os.path.join(output_path, '{}.conf'.format(args.type))
        if os.path.exists(output_path):
            self.stderr.write("ERROR! output file already exists: {}\n".format(output_path))
            sys.exit(2)

        config_path = self.app.make_config_file(args.type, output_path,
                                                template_path=template_path)
        self.stdout.write("Config file generated at: {}\n".format(config_path))

    def list_types(self):
        templates = self.app.get_all_config_templates()
        self.stdout.write("CONFIG TEMPLATES:\n")
        self.stdout.write("=========================\n")
        for name, path in templates.items():
            self.stdout.write("{:25s} {}\n".format(name, path))
        self.stdout.write("=========================\n")


class MakeUser(Subcommand):
    """
    Create a new user account in a given system
    """
    name = 'make-user'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('username',
                            help="Username for the new user.")
        parser.add_argument('--system', default='rattail',
                            help="System in which to create the new user; defaults to "
                            "rattail; must be one of: rattail, windows")
        parser.add_argument('-A', '--admin', action='store_true',
                            help="Whether the new user should have admin rights within "
                            "the system (if applicable).")
        parser.add_argument('--password',
                            help="Password to set for the new user.  If not specified, "
                            "you may be prompted for one.")
        parser.add_argument('--no-password', action='store_true',
                            help="Do not ask for, or try to set, a password for the new user.")
        parser.add_argument('--full-name',
                            help="Full (display) name for the new user (if applicable).")
        parser.add_argument('--comment',
                            help="Comment string for the new user (if applicable).")
        parser.add_argument('--groups',
                            help="Optional list of groups (roles) to which the new user "
                            "should be assigned.")

    def run(self, args):
        mkuser = getattr(self, 'mkuser_{}'.format(args.system), None)
        if mkuser:
            if mkuser(args):
                self.stdout.write("created new user in '{}' system: {}\n".format(
                    args.system, args.username))
        else:
            self.stderr.write("don't know how to make user for '{}' system\n".format(args.system))
            sys.exit(1)

    def user_exists(self, args):
        self.stdout.write("user already exists in '{}' system: {}\n".format(
            args.system, args.username))
        sys.exit(1)

    def obtain_password(self, args):
        if args.password:
            return args.password
        try:
            password = None
            while not password:
                password = getpass(str("enter password for new user: ")).strip()
        except KeyboardInterrupt:
            self.stderr.write("\noperation canceled by user\n")
            sys.exit(2)
        return password

    def mkuser_rattail(self, args):
        from sqlalchemy import orm
        from rattail.db import auth

        session = self.make_session()
        model = self.parent.db_model
        if session.query(model.User).filter_by(username=args.username).count():
            session.close()
            return self.user_exists(args)

        roles = []
        if args.groups:
            for name in parse_list(args.groups):
                try:
                    role = session.query(model.Role)\
                                  .filter(model.Role.name == name)\
                                  .one()
                except orm.exc.NoResultFound:
                    self.stderr.write("Role not found: {}\n".format(name))
                    session.close()
                    sys.exit(4)
                else:
                    roles.append(role)

        user = model.User(username=args.username)
        if not args.no_password:
            auth.set_user_password(user, self.obtain_password(args))

        if args.admin:
            user.roles.append(auth.administrator_role(session))
        for role in roles:
            user.roles.append(role)

        if args.full_name:
            kwargs = {'display_name': args.full_name}
            words = args.full_name.split()
            if len(words) == 2:
                kwargs.update({'first_name': words[0], 'last_name': words[1]})
            user.person = model.Person(**kwargs)

        session.add(user)
        session.commit()
        session.close()
        return True

    def mkuser_windows(self, args):
        if sys.platform != 'win32':
            self.stderr.write("sorry, only win32 platform is supported\n")
            sys.exit(1)

        from rattail.win32 import users
        from rattail.win32 import require_elevation

        if args.no_password:
            self.stderr.write("sorry, a password is required when making a 'win32' user\n")
            sys.exit(1)

        require_elevation()

        if users.user_exists(args.username):
            return self.user_exists(args)

        return users.create_user(args.username, self.obtain_password(args),
                                 full_name=args.full_name, comment=args.comment)


class MakeUUID(Subcommand):
    """
    Generate a new UUID
    """
    name = 'make-uuid'
    description = __doc__.strip()

    def run(self, args):
        from rattail.core import get_uuid

        self.stdout.write("{}\n".format(get_uuid()))


class PalmCommand(Subcommand):
    """
    Manages registration for the HotSync Manager conduit; called as::

       rattail palm
    """

    name = 'palm'
    description = "Manage the HotSync Manager conduit registration"

    def add_parser_args(self, parser):
        subparsers = parser.add_subparsers(title='subcommands')

        register = subparsers.add_parser('register', help="Register Rattail conduit")
        register.set_defaults(subcommand='register')

        unregister = subparsers.add_parser('unregister', help="Unregister Rattail conduit")
        unregister.set_defaults(subcommand='unregister')

    def run(self, args):
        from rattail import palm
        from rattail.win32 import require_elevation
        from rattail.exceptions import PalmError

        require_elevation()

        if args.subcommand == 'register':
            try:
                palm.register_conduit()
            except PalmError as error:
                sys.stderr.write("{}\n".format(error))

        elif args.subcommand == 'unregister':
            try:
                palm.unregister_conduit()
            except PalmError as error:
                sys.stderr.write("{}\n".format(error))
                

class RunAndMail(Subcommand):
    """
    Run a command as subprocess, and email the result/output
    """
    name = 'run-n-mail'
    description = __doc__.strip()

    def add_parser_args(self, parser):

        parser.add_argument('--skip-if-empty', action='store_true',
                            help="Skip sending the email if the command generates no output.")

        parser.add_argument('--key', default='run_n_mail',
                            help="Config key for email settings")
        # TODO: these all seem like good ideas, but not needed yet?
        # parser.add_argument('--from', '-F', metavar='ADDRESS',
        #                     help="Override value of From: header")
        # parser.add_argument('--to', '-T', metavar='ADDRESS',
        #                     help="Override value of To: header (may specify more than once)")
        # parser.add_argument('--cc', metavar='ADDRESS',
        #                     help="Override value of Cc: header (may specify more than once)")
        # parser.add_argument('--bcc', metavar='ADDRESS',
        #                     help="Override value of Bcc: header (may specify more than once)")
        parser.add_argument('--subject', '-S',
                            help="Override value of Subject: header (i.e. value after prefix)")
        parser.add_argument('cmd', metavar='COMMAND',
                            help="Command which should be ran, and result of which will be emailed")

        parser.add_argument('--keep-exit-code', action='store_true',
                            help="Exit with same return code as subprocess.  If "
                            "this is not specified, `run-n-mail` will normally "
                            "exit with code 0 regardless of what happens with "
                            "the subprocess.")

    def run(self, args):
        cmd = parse_list(args.cmd)
        log.info("will run command as subprocess: %s", cmd)
        run_began = self.app.make_utc()

        try:
            # TODO: must we allow for shell=True in some situations? (clearly not yet)
            output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            retcode = 0
            log.info("command completed successfully")
        except subprocess.CalledProcessError as error:
            output = error.output
            retcode = error.returncode
            log.warning("command exited with code: %s", retcode)

        output = output.decode(errors='replace')

        run_ended = self.app.make_utc()
        runtime = run_ended - run_began
        runtime_pretty = humanize.naturaldelta(runtime)

        if args.skip_if_empty and not output:
            log.info("command had no output, so will skip sending email")
            # return

        else: # send email
            kwargs = {}
            if args.subject:
                kwargs['subject_template'] = args.subject
            self.app.send_email(args.key, {
                'cmd': cmd,
                'run_began': run_began,
                'run_ended': run_ended,
                'runtime': runtime,
                'runtime_pretty': runtime_pretty,
                'retcode': retcode,
                'output': output,
            }, **kwargs)

        if retcode and args.keep_exit_code:
            sys.exit(retcode)


class RunSQL(Subcommand):
    """
    Run (first statement of) a SQL script against a database
    """
    name = 'runsql'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('engine',
                            help="SQLAlchemy engine URL for the database.")
        parser.add_argument('script', type=argparse.FileType('r'),
                            help="Path to file which contains a SQL script.")
        parser.add_argument('--max-width', type=int, default=80,
                            help="Max table width when displaying results.")

    def run(self, args):
        import sqlalchemy as sa
        import texttable

        sql = []
        for line in args.script:
            line = line.strip()
            if line and not line.startswith('--'):
                sql.append(line)
                if line.endswith(';'):
                    break

        sql = ' '.join(sql)
        engine = sa.create_engine(args.engine)

        with engine.begin() as cxn:
            result = cxn.execute(sa.text(sql))
            rows = result.fetchall()
            if rows:
                table = texttable.Texttable(max_width=args.max_width)

                # force all columns to be treated as text.  that seems a bit
                # heavy-handed but is definitely the simplest way to deal with
                # issues such as a UPC being displayed in scientific notation
                table.set_cols_dtype(['t' for col in rows[0]])

                # add a header row, plus all data rows
                table.add_rows([rows[0].keys()] + rows)

                self.stdout.write("{}\n".format(table.draw()))


class Upgrade(Subcommand):
    """
    Upgrade the local Rattail app
    """
    name = 'upgrade'
    description = __doc__.strip()

    def add_parser_args(self, parser):
        parser.add_argument('--system', default='rattail',
                            help="System to which the upgrade applies.")

        parser.add_argument('--description',
                            help="Description for the new/matched upgrade.")
        parser.add_argument('--enabled', action='store_true', default=True,
                            help="Indicate the enabled flag should be ON for the new/matched upgrade.  "
                            "Note that this is the default if you do not specify.")
        parser.add_argument('--no-enabled', action='store_false', dest='enabled',
                            help="Indicate the enabled flag should be OFF for the new/matched upgrade.")
        parser.add_argument('--create', action='store_true',
                            help="Create a new upgrade with the given attributes.")
        parser.add_argument('--execute', action='store_true',
                            help="Execute the upgrade.  Note that if you do not specify "
                            "--create then the upgrade matching the given attributes "
                            "will be read from the database.  If such an upgrade is not "
                            "found or is otherwise invalid (e.g. already executed), "
                            "the command will fail.")

        parser.add_argument('--keep-exit-code', action='store_true',
                            help="Exit with same return code as subprocess.  If "
                            "this is not specified, this command will normally "
                            "exit with code 0 regardless of what happens with "
                            "the subprocess.  (only applicable with --execute)")

        parser.add_argument('--dry-run', action='store_true',
                            help="Go through the full motions and allow logging etc. to "
                            "occur, but rollback (abort) the transaction at the end.")

    def run(self, args):
        from sqlalchemy import orm

        if not args.create and not args.execute:
            self.stderr.write("Must specify --create and/or --execute\n")
            sys.exit(1)

        session = self.make_session()
        model = self.model
        user = self.get_runas_user(session)

        if args.create:
            upgrade = model.Upgrade()
            upgrade.system = args.system or 'rattail'
            upgrade.description = args.description
            upgrade.created = self.app.make_utc()
            upgrade.created_by = user
            upgrade.enabled = args.enabled
            session.add(upgrade)
            session.flush()
            log.info("user '%s' created new upgrade: %s", user.username, upgrade)

        else:
            upgrades = session.query(model.Upgrade)\
                              .filter(model.Upgrade.enabled == args.enabled)
            if args.description:
                upgrades = upgrades.filter(model.Upgrade.description == args.description)
            try:
                upgrade = upgrades.one()
            except orm.exc.NoResultFound:
                self.stderr.write("no matching upgrade found\n")
                session.rollback()
                session.close()
                sys.exit(1)
            except orm.exc.MultipleResultsFound:
                self.stderr.write("found {} matching upgrades\n".format(upgrades.count()))
                session.rollback()
                session.close()
                sys.exit(1)

        if args.execute:
            if upgrade.executed:
                self.stderr.write("upgrade has already been executed: {}\n".format(upgrade))
                session.rollback()
                session.close()
                sys.exit(1)
            if not upgrade.enabled:
                self.stderr.write("upgrade is not enabled for execution: {}\n".format(upgrade))
                session.rollback()
                session.close()
                sys.exit(1)

            # execute upgrade
            handler = self.app.get_upgrade_handler()
            log.info("will now execute upgrade: %s", upgrade)
            if not args.dry_run:
                handler.mark_executing(upgrade)
                session.commit()
                handler.do_execute(upgrade, user, progress=self.progress)
            log.info("user '%s' executed upgrade: %s", user.username, upgrade)

        if args.dry_run:
            session.rollback()
            log.info("dry run, so transaction was rolled back")
        else:
            session.commit()
            log.info("transaction was committed")
        session.close()

        if (args.execute and not args.dry_run
            and args.keep_exit_code and upgrade.exit_code):
            sys.exit(upgrade.exit_code)


def main(*args):
    """
    The primary entry point for the Rattail command system.
    """
    if args:
        args = list(args)
    else:
        args = sys.argv[1:]

    cmd = Command()
    cmd.run(*args)
