# Copyright (c) 2014 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


"""
This script presents a python example of logging into a steelhead
appliance to print the states of the steelhead as in python data structures.
"""

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

import steelscript.steelhead.core.steelhead as steelhead

from pprint import pprint
from steelscript.common.app import Application
from steelscript.common.interaction.action import Action
from steelscript.common.interaction.model import Model


class SteelHeadAPIApp(Application):
    def add_positional_args(self):
        self.add_positional_arg('host', 'SteelHead hostname or IP address')

    def add_options(self, parser):
        super(SteelHeadAPIApp, self).add_options(parser)

        parser.add_option('-u', '--username', help="Username to connect with")
        parser.add_option('-p', '--password', help="Password to use")

    def validate_args(self):
        super(SteelHeadAPIApp, self).validate_args()

        if not self.options.username:
            self.parser.error("User Name needs to be specified")

        if not self.options.password:
            self.parser.error("Password needs to be specified")

    def main(self):
        auth = steelhead.CLIAuth(username=self.options.username,
                                 password=self.options.password)
        sh = steelhead.SteelHead(host=self.options.host, auth=auth)

        print("\n*****Version**********\n")
        version_model = Model.get(sh, feature='common')
        pprint(version_model.show_version())

        print("\n*****Networking State**********\n")
        networking_model = Model.get(sh, feature='networking')
        pprint(networking_model.show_interfaces("aux"))

        print("\n********All Current Flows*********\n")
        flows_model = Model.get(sh, feature='flows')
        pprint(flows_model.show_flows('all'))

        # Use the Action class
        flows_action = Action.get(sh, feature='flows')
        print("\n********All Optimized Flows*********\n")
        pprint(flows_action.show_flows_optimized())
        print("\n********All Passthrough Flows***********\n")
        pprint(flows_action.show_flows_passthrough())

        print ("\n********Bandwidth Statistics*********\n")
        stats_model = Model.get(sh, feature='stats')
        pprint(stats_model.show_stats_bandwidth('all', 'bi-directional',
                                                '5min'))


if __name__ == '__main__':
    SteelHeadAPIApp().run()
