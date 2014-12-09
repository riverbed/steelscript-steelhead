# -*- coding: utf-8 -*-
#
# Copyright 2014 Riverbed Technology, Inc.
# All Rights Reserved. Confidential.

from __future__ import (unicode_literals, print_function, division,
                        absolute_import)

from steelscript.common.interaction import action, uidelegation


@action.action
class FlowsAction(action.Action):
    """
    Kauai Flows Actions for SteelHead product
    """


class CLI(uidelegation.CLI):
    """
    Kauai Reporting CLI Delegatee
    """

    def show_flows_optimized(self):
            return self.model.show_flows(type="optimized")

    def show_flows_passthrough(self):
            return self.model.show_flows(type="passthrough")
