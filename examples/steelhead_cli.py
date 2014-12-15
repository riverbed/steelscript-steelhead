# Copyright (c) 2014 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


"""
This script presents a python example of logging into a steelhead
appliance to show version, networking state, current connections
(flows) and bandwidth statistics.
"""

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

import steelscript.steelhead.core.steelhead as steelhead

from steelscript.common.app import Application


class SteelHeadCLIApp(Application):
    def add_positional_args(self):
        self.add_positional_arg('host', 'SteelHead hostname or IP address')

    def add_options(self, parser):
        super(SteelHeadCLIApp, self).add_options(parser)

        parser.add_option('-u', '--username', help="Username to connect with")
        parser.add_option('-p', '--password', help="Password to use")

    def validate_args(self):
        super(SteelHeadCLIApp, self).validate_args()

        if not self.options.username:
            self.parser.error("User Name needs to be specified")

        if not self.options.password:
            self.parser.error("Password needs to be specified")

    def main(self):
        auth = steelhead.CLIAuth(username=self.options.username,
                                 password=self.options.password)
        sh = steelhead.SteelHead(host=self.options.host, auth=auth)

        print("\n*****Version**********\n")
        print(sh.cli.exec_command("show version"))

        print("\n*****Networking State**********\n")
        print(sh.cli.exec_command("show interfaces aux"))

        print("\n********All Current Flows*********\n")
        print(sh.cli.exec_command("show flows all"))
        print("\n********All Optimized Flows*********\n")
        print(sh.cli.exec_command("show flows optimized"))
        print("\n********All Passthrough Flows***********\n")
        print(sh.cli.exec_command("show flows passthrough"))

        print ("\n********Bandwidth Statistics*********\n")
        print (sh.cli.exec_command("show stats bandwidth all "
                                   "bi-directional 5min"))

if __name__ == '__main__':
    SteelHeadCLIApp().run()
