# Copyright (c) 2014 Riverbed Technology, Inc.
#
# This software is licensed under the terms and conditions of the MIT License
# accompanying the software ("License").  This software is distributed "AS IS"
# as set forth in the License.

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

# TODO
from steelscript.common.features.model import model, Model
#from steelscript.common import Model
from steelscript.cmdline.parsers import cli_parse_basic


@model
class OptimizationModel(Model):
    """
    Kauai Optimization model for the SteelHead product
    """

    def enable(self):
        """
        Enables Optimization service

            service enable
        """
        return self.cli.exec_command("service enable", output_expected=True)

    def disable(self):
        """
        Disables Optimization service

            no service enable
        """
        return self.cli.exec_command("no service enable", output_expected=True)

    def restart(self):
        """
        Restart service, but do not wait for it to come up

            service restart
        """
        return self.cli.exec_command("service restart", output_expected=True)

    def show(self):
        """
        Gets information about the optimization service

            show service

        :return: A dictionary of parsed output
        """
        output = self.cli.exec_command("show service", output_expected=True)
        return cli_parse_basic(output)

    def show_sport_intercept(self):
        """
        Return parsed output of 'show sport intercept ready'

        Intercept Module Ready: yes

        :return: {'intercept module ready': True}
        """
        cmd = "show sport intercept ready"
        output = self.cli.exec_command(cmd, output_expected=True)
        return cli_parse_basic(output)
