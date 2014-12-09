# -*- coding: utf-8 -*-
#
# Copyright 2014 Riverbed Technology, Inc.
# All Rights Reserved. Confidential.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

from steelscript.common.interaction.model import model, Model
from steelscript.cmdline.parsers import cli_parse_basic

import re

@model
class StatsModel(Model):
    """
    Kauai Stats model for the SteelHead product
    """

    def show_stats_bandwidth(self, port='all', type=None, frequency=None):
        """
        Method to show Bandwidth Stats on a SteelHead

        :param port: Optional parameter to filter the bandwidth summary to
                     traffic on a specific port.  The value is simply the port
                     number (e.g., "80") and defaults to "all."
        :type port: string

        :param type: The type of traffic to summarize.  Options include
                     bi-directional, lan-to-wan, and wan-to-lan.
        :type type: string

        :param frequency: Last period of time to lookback during stats
                          collection.  Options include 1min, 5min, hour, day,
                          week, or month.
        :type period: string

        :return: dictionary {
                    'wan data': '5.4 GB',
                    'lan data': '6 GB',
                    'data reduction': '10 %',
                    'data reduction peak': '95 %',
                    'data reduction peak time': '2014/12/05 14:50:00',
                    'capacity increase': '1.1 X'}
        """

        cmd = "show stats bandwidth %s" % port
        if type is not None:
            cmd = cmd + " " + type
        if frequency is not None:
            cmd = cmd + " " + frequency
        result = self.cli.exec_command(cmd, output_expected=True)

        return cli_parse_basic(result)

