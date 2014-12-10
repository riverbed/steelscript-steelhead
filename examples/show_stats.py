# Copyright (c) 2014 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.


"""
This script presents a python example of logging into a steelhead
appliance to print the current bandwidth statistics.
"""

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

from steelscript.common.app import Application
from steelscript.steelhead.core import CLIAuth, SteelHead
from steelscript.common.interaction.model import Model


class ShowVersionApp(Application):

    def add_options(self, parser):
        super(ShowVersionApp, self).add_options(parser)

        parser.add_option('-H', '--host',
                          help='hostname or IP address')
        parser.add_option('-u', '--username', help="Username to connect with")
        parser.add_option('-p', '--password', help="Password to use")

    def validate_args(self):
        super(ShowVersionApp, self).validate_args()

        if not self.options.host:
            self.parser.error("Host name needs to be specified")

        if not self.options.username:
            self.parser.error("User Name needs to be specified")

        if not self.options.password:
            self.parser.error("Password needs to be specified")

    def main(self):
        auth = CLIAuth(username=self.options.username,
                       password=self.options.password)
        sh = SteelHead(host=self.options.host, auth=auth)

        # Using the model class
        print("\nStats")
        stats_model = Model.get(sh, feature='stats')
        print(stats_model.show_stats_bandwidth('all',
                                               'bi-directional',
                                               '5min'))

if __name__ == '__main__':
    ShowVersionApp().run()
