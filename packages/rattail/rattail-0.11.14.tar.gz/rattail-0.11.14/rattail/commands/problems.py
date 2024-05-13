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
Problem Report Commands
"""

from rattail.commands import Subcommand


class Problems(Subcommand):
    """
    Find and/or fix, and report on problems with the data
    """
    name = 'problems'
    description = __doc__.strip()

    def add_args(self):
        """ """
        super().add_args()
        parser = self.parser

        parser.add_argument('--system', '-s', dest='systems', metavar='KEY', action='append',
                            help="System for which problem checks should be performed.  You "
                            "may specify this more than once, to check multiple systems.  If "
                            "not specified, all supported systems will be checked.")

        parser.add_argument('--problem', '-p', dest='problems', metavar='KEY', action='append',
                            help="Identifies a particular problem check which should be performed.  "
                            "You may specify this more than once, to check multiple problems.  If "
                            "not specified, all supported problem reports will run.")

        parser.add_argument('--list', '-l', action='store_true',
                            help="List available problem reports, instead of running them.  "
                            "If --system args are present, will only show those reports.")

        parser.add_argument('--fix', '-F', action='store_true',
                            help="Whether to (attempt to) fix the problems, vs. just reporting them.")

        parser.add_argument('--force', action='store_true',
                            help="Force running of the report(s), i.e. ignore "
                            "the \"enabled\" and scheduling flags.")

        parser.add_argument('--dry-run', action='store_true',
                            help="Go through the full motions and allow logging etc. to "
                            "occur, but rollback (abort) the transaction at the end.")

    def run(self, args):
        handler = self.app.get_problem_report_handler(dry_run=args.dry_run,
                                                      progress=self.progress)

        # try to warn user if unknown system is specified; but otherwise ignore
        supported_systems = handler.supported_systems()
        for key in (args.systems or []):
            if key not in supported_systems:
                self.stderr.write("No problem reports exist for system: {}\n".format(key))

        reports = handler.get_problem_reports(systems=args.systems,
                                              problems=args.problems)

        if args.list:
            self.list_reports(handler, reports)
        else:
            handler.run_problem_reports(reports, fix=args.fix, force=args.force)

    def list_reports(self, handler, reports):
        """
        List all relevant problem reports.
        """
        organized = handler.organize_problem_reports(reports)
        for system in sorted(organized):

            self.stdout.write("\n{}\n".format(system))
            self.stdout.write("-------------------------\n")
            for problem in sorted(organized[system]):
                self.stdout.write("{}\n".format(problem))

        self.stdout.write("\n")
