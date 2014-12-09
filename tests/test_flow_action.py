# -*- coding: utf-8 -*-
#
# Copyright 2014 Riverbed Technology, Inc.
# All Rights Reserved. Confidential.
from __future__ import unicode_literals
import mock
import pytest

from steelscript.common.interaction import action, uidelegation
from steelscript.steelhead.features.flows.v8_5.action import FlowsAction as CommonFlows


SHOW_FLOWS_PASSTHROUGH = """\
T  Source                Destination           App     Rdn Since              
--------------------------------------------------------------------------------
PI 10.3.2.54:40097       10.190.174.120:443    TCP     2014/01/02 06:00:50
PI 10.3.2.23:52618       10.190.174.121:443    TCP     2014/01/02 14:06:09
PI 10.18.32.131:49671    10.190.1.233:3389     TCP     2014/01/02 10:09:04
PI 10.3.2.24:42797       10.190.174.122:443    TCP     2014/01/02 13:58:04
PI 10.3.1.87:13729       10.190.174.123:443    TCP     2014/01/02 04:14:06
--------------------------------------------------------------------------------
                                           All    V4     V6
---------------------------------------------------------------
Passthrough :                              11     22     33

  Passthrough intentional (PI):            1      2      3
  Passthrough unintentional (PU):          11     22     33

    Terminated:                            1      2      3
    Packet-mode:                           11     22     33

Forwarded (F):                             1      2      3
---------------------------------------------------------------

Total:                                     11     40      70
"""


SHOW_FLOWS_PASSTHROUGH_PARSED = {
    'flows_list': [
        {'app': 'TCP',
         'destination ip': '10.190.174.120',
         'destination port': '443',
         'percent': '',
         'since': {'day': '02',
                   'hour': '06',
                   'min': '00',
                   'month': '01',
                   'secs': '50',
                   'year': '2014'},
         'source ip': '10.3.2.54',
         'source port': '40097',
         'type': 'PI'},
        {'app': 'TCP',
         'destination ip': '10.190.174.121',
         'destination port': '443',
         'percent': '',
         'since': {'day': '02',
                    'hour': '14',
                    'min': '06',
                    'month': '01',
                    'secs': '09',
                    'year': '2014'},
         'source ip': '10.3.2.23',
         'source port': '52618',
         'type': 'PI'},
        {'app': 'TCP',
         'destination ip': '10.190.1.233',
         'destination port': '3389',
         'percent': '',
         'since': {'day': '02',
                   'hour': '10',
                   'min': '09',
                   'month': '01',
                   'secs': '04',
                   'year': '2014'},
         'source ip': '10.18.32.131',
         'source port': '49671',
         'type': 'PI'},
        {'app': 'TCP',
         'destination ip': '10.190.174.122',
         'destination port': '443',
         'percent': '',
         'since': {'day': '02',
                   'hour': '13',
                   'min': '58',
                   'month': '01',
                   'secs': '04',
                   'year': '2014'},
         'source ip': '10.3.2.24',
         'source port': '42797',
         'type': 'PI'},
        {'app': 'TCP',
         'destination ip': '10.190.174.123',
         'destination port': '443',
         'percent': '',
         'since': {'day': '02',
                   'hour': '04',
                   'min': '14',
                   'month': '01',
                   'secs': '06',
                   'year': '2014'},
         'source ip': '10.3.1.87',
         'source port': '13729',
         'type': 'PI'},
    ],
    'flows_summary': {
        'forwarded': {'all': '1', 'v4': '2', 'v6': '3'},
        'passthrough': {'all': '11', 'v4': '22', 'v6': '33'},
        'passthrough intentional': {'all': '1', 'v4': '2', 'v6': '3'},
        'passthrough unintentional': {'all': '11', 'v4': '22', 'v6': '33'},
        'passthrough unintentional packet_mode': {'all': '11',
                                                  'v4': '22',
                                                  'v6': '33'},
        'passthrough unintentional terminated': {'all': '1',
                                                 'v4': '2',
                                                 'v6': '3'},
        'total': {u'all': u'11', u'v4': u'40', u'v6': u'70'}}
}

SHOW_FLOWS_OPTIMIZED = """\
T  Source                Destination           App     Rdn Since
--------------------------------------------------------------------------------
N  10.190.0.1:406        10.190.5.2:1003       UDPv4   99% 2014/02/10 23:58:01
O  192.168.0.1:80        192.168.5.1:80        SRDF_V2 11% 2014/02/01 00:00:01
O  192.168.221.1:1080    192.168.221.1:1080    CIFS     0% 2014/02/01 00:20:01
O  192.168.221.1:443     192.168.221.1:443     MAPI    99% 2014/02/01 00:21:01
N  192.168.221.1:1443    192.168.221.1:5543    TCPv4   99% 2014/02/10 23:56:01
N  10.190.0.1:1406       10.190.5.2:2003       FTP-DAT 59% 2014/02/01 00:00:01
--------------------------------------------------------------------------------
                                           All    V4     V6
---------------------------------------------------------------
Established Optimized:                     1      2      3

  RiOS Only (O):                           1      3      3
  SCPS Only (SO):                          11     22     33
  RiOS+SCPS (RS):                          1      2      3
  TCP Proxy (TP):                          1      2      3
  Packet-mode optimized (N):               11     22     33
---------------------------------------------------------------

Total:                                     11     40      70
"""


SHOW_FLOWS_OPTIMIZED_PARSED = {
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
         'type': 'N'},
        {'app': 'SRDF_V2',
         'destination ip': '192.168.5.1',
         'destination port': '80',
         'percent': '11',
         'since': {'day': '01',
                    'hour': '00',
                    'min': '00',
                    'month': '02',
                    'secs': '01',
                    'year': '2014'},
         'source ip': '192.168.0.1',
         'source port': '80',
         'type': 'O'},
        {'app': 'CIFS',
         'destination ip': '192.168.221.1',
         'destination port': '1080',
         'percent': '0',
         'since': {'day': '01',
                   'hour': '00',
                   'min': '20',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': '192.168.221.1',
         'source port': '1080',
         'type': 'O'},
        {'app': 'MAPI',
         'destination ip': '192.168.221.1',
         'destination port': '443',
         'percent': '99',
         'since': {'day': '01',
                   'hour': '00',
                   'min': '21',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': '192.168.221.1',
         'source port': '443',
         'type': 'O'},
        {'app': 'TCPv4',
         'destination ip': '192.168.221.1',
         'destination port': '5543',
         'percent': '99',
         'since': {'day': '10',
                   'hour': '23',
                   'min': '56',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': '192.168.221.1',
         'source port': '1443',
         'type': 'N'},
        {'app': 'FTP-DAT',
         'destination ip': '10.190.5.2',
         'destination port': '2003',
         'percent': '59',
         'since': {'day': '01',
                   'hour': '00',
                   'min': '00',
                   'month': '02',
                   'secs': '01',
                   'year': '2014'},
         'source ip': '10.190.0.1',
         'source port': '1406',
         'type': 'N'}
    ],
    'flows_summary': {
        'established optimized': {'all': '1', 'v4': '2', 'v6': '3'},
        'packet_mode optimized': {'all': '11', 'v4': '22', 'v6': '33'},
        'rios only': {'all': '1', 'v4': '3', 'v6': '3'},
        'rios scps': {'all': '1', 'v4': '2', 'v6': '3'},
        'scps only': {'all': '11', 'v4': '22', 'v6': '33'},
        'tcp proxy': {'all': '1', 'v4': '2', 'v6': '3'},
        'total': {u'all': u'11', u'v4': u'40', u'v6': u'70'}}
}

@pytest.yield_fixture
def mock_cli():
    with mock.patch('steelscript.common.interaction.model.Model.cli') as mock_cli:
        yield mock_cli


def test_show_flows_passthrough(mock_cli):
    actor = action.Action.get(mock.Mock, feature="flows")
    mock_cli.exec_command.return_value = SHOW_FLOWS_PASSTHROUGH
    result = actor.show_flows_passthrough()
    assert result['flows_list'] == SHOW_FLOWS_PASSTHROUGH_PARSED['flows_list']
    assert result['flows_summary'] == SHOW_FLOWS_PASSTHROUGH_PARSED['flows_summary']

def test_show_flows_optimized(mock_cli):
    actor = action.Action.get(mock.Mock, feature="flows")
    mock_cli.exec_command.return_value = SHOW_FLOWS_OPTIMIZED
    result = actor.show_flows_optimized()
    assert result['flows_list'] == SHOW_FLOWS_OPTIMIZED_PARSED['flows_list']
    assert result['flows_summary'] == SHOW_FLOWS_OPTIMIZED_PARSED['flows_summary']
