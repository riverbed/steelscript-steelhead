# -*- coding: utf-8 -*-
#
# Copyright 2014 Riverbed Technology, Inc.
# All Rights Reserved. Confidential.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

from steelscript.common.interaction.model import model, Model

import re


@model
class FlowsModel(Model):
    """
    Kauai Flows model for the SteelHead product
    """

    def parse_flow_summary(self, output):
        # group 1
        type_pattern = "([a-zA-Z]+)"
        # group 2-5 (src/dst)
        # TODO: need to handle IPv6
        ipv4_port_pattern = "(\d+\.\d+\.\d+\.\d+):(\d+)"
        # group 6
        app_pattern = "(.+?)"
        # group 7 - this only shows up for optimized connections
        percent_pattern = "(\d*)%*"
        # group 8-13
        # TODO: instaed of a date+time, this can be a string (pre_existing)
        since_pattern = "(\d+)\/(\d+)\/(\d+)\s+(\d+):(\d+):(\d+)"

        flow_pattern = "%s\s+%s\s+%s\s+%s\s+%s\s+%s\s*$" \
                       % (type_pattern, ipv4_port_pattern, ipv4_port_pattern,
                          app_pattern, percent_pattern, since_pattern)

        flow_info_dict = None
        regex = re.compile(flow_pattern)
        match = regex.search(output)
        if match:
            flow_info_dict = dict()
            flow_info_dict = {'type': match.group(1),
                              'source ip': match.group(2),
                              'source port': match.group(3),
                              'destination ip': match.group(4),
                              'destination port': match.group(5),
                              'app': match.group(6),
                              'percent': match.group(7),
                              'since': {'year': match.group(8),
                                        'month': match.group(9),
                                        'day': match.group(10),
                                        'hour': match.group(11),
                                        'min': match.group(12),
                                        'secs': match.group(13)}}
        return flow_info_dict

    def show_flows(self, type='all'):
        """
        Method to show Flows on a SteelHead

        :param type: Optional parameter to select the type of Flows.  Valid
                     choices include all, optimized, passthrough, packet-mode,
                     and tcp-term.
        :type type: string

        :return: dictionary {
                'flows_list': [
                    {'app': 'UDPv4',
                    'destination ip': '10.190.5.2',
                    'destination port': '1003',
                    'percent': '99',
                    'since': {'day': '10',
                              'hour': '23',
                              'min': '58',
                              'month': '02',
                              'secs': '01',
                              'year': '2014'},
                    'source ip': '10.190.0.1',
                    'source port': '406',
                    'type': 'N'},...],
                'flows_summary': {
                    'denied': {'all': '1'},
                    'discarded': {'all': '1'},
                    'establishing': {'all': '1', 'v4': '2', 'v6': '3'},
                    'forwarded': {'all': '1', 'v4': '2', 'v6': '3'},
                    'half_closed optimized':
                        {'all': '11', 'v4': '22', 'v6': '33'},
                    'half_opened optimized':
                        {'all': '1', 'v4': '2', 'v6': '3'},
                    'optimized': {'all': '1', 'v4': '2', 'v6': '3'},
                    'packet_mode optimized':
                        {'all': '11', 'v4': '22', 'v6': '33'},
                    'passthrough': {'all': '11', 'v4': '22', 'v6': '33'},
                    'passthrough intentional':
                        {'all': '1', 'v4': '2', 'v6': '3'},
                    'passthrough unintentional':
                        {'all': '11', 'v4': '22', 'v6': '33'},
                    'passthrough unintentional packet_mode':
                        {'all': '11', 'v4': '22', 'v6': '33'},
                    'passthrough unintentional terminated':
                        {'all': '1', 'v4': '2', 'v6': '3'},
                    'rios only': {'all': '1', 'v4': '3', 'v6': '3'},
                    'rios scps': {'all': '1', 'v4': '2', 'v6': '3'},
                    'scps only': {'all': '11', 'v4': '22', 'v6': '33'},
                    'tcp proxy': {'all': '1', 'v4': '2', 'v6': '3'},
                    'total': {'all': '1', 'v4': '2', 'v6': '3'}}
        """

        cmd = "show flows %s" % type
        result = self.cli.exec_command(cmd, output_expected=True)

        # Parse show flows all cmd output
        lines = result.splitlines()

        title_parsed = False
        title_pattern = "T\s+Source\s+Destination\s+App\s+Rdn\s+Since"
        title_regex = re.compile(title_pattern)

        flows_list = []
        flows_summary_dict = dict()

        summary_list = {'Established Optimized': 'established optimized',
                        'RiOS Only (O)': 'rios only',
                        'SCPS Only (SO)': 'scps only',
                        'RiOS+SCPS (RS)': 'rios scps',
                        'TCP Proxy (TP)': 'tcp proxy',
                        'Packet-mode optimized (N)': 'packet_mode optimized',
                        'Half-opened optimized (H)': 'half_opened optimized',
                        'Half-closed optimized (C)': 'half_closed optimized',
                        'Establishing (E)': 'establishing',
                        'Passthrough': 'passthrough',
                        'Passthrough intentional (PI)':
                            'passthrough intentional',
                        'Passthrough unintentional (PU)':
                            'passthrough unintentional',
                        'Terminated': 'passthrough unintentional terminated',
                        'Packet-mode': 'passthrough unintentional packet_mode',
                        'Forwarded (F)': 'forwarded',
                        'Discarded (terminated)': 'discarded',
                        'Denied (terminated)': 'denied',
                        'Total': 'total'}

        for line in lines:
            # Skip empty line
            if not len(line):
                continue

            # Parse Title
            if title_parsed is not True:
                match = title_regex.search(line)
                if match:
                    title_parsed = True
                    # Done parsing Title
                    continue

            # Skip "-----------..." lines
            match = re.match(r'^-+$', line)
            if match:
                continue

            # Parse connections/flows
            flow_info_dict = self.parse_flow_summary(line)
            if flow_info_dict:
                flows_list.append(flow_info_dict)
                continue

            # Parse Summary report
            items = line.split(':')
            for category in summary_list:
                output = items[0].strip()
                exp_output = category.strip()
                if output == exp_output:
                    match = re.match('\s+(\d+)\s+(\d+)\s+(\d+)\s*$', items[1])
                    if match:
                        flows_summary_dict[summary_list[category]] = \
                            {'all': match.group(1),
                             'v4': match.group(2),
                             'v6': match.group(3)}
                        break
                    match = re.match('\s+(\d+)$', items[1])
                    if match:
                        flows_summary_dict[summary_list[category]] = \
                            {'all': match.group(1)}
                        break

        output = {'flows_list': flows_list,
                  'flows_summary': flows_summary_dict}
        return output
