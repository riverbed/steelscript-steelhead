# -*- coding: utf-8 -*-
#
# Copyright 2014 Riverbed Technology, Inc.
# All Rights Reserved. Confidential.

from __future__ import (absolute_import, unicode_literals, print_function,
                        division)

#from pq_runtime import extension
from steelscript.common.features import action, uidelegation
#from pq_sh.services.optimization.kauai.model import Kauai as Model
#from pq_runtime import polling


@action.action
class OptimizationAction(action.Action):

    """
    Kauai Optimization Actions for SteelHead product
    """


#@extension.extend_class(Model, 'model', method_list=[
#    'enable', 'disable', 'restart', 'show', 'show_sport_intercept'])
class CLI(uidelegation.CLI):

    """
    Kauai Optimization for Actions for the SteelHead product.
    """

    def show(self):
        return self.model.show()

#    def is_sport_intercept_ready(self, max_retries=20, min_interval=3):
#        """
#        Note:  This method is deprecated.  Instead use:
#               Verification.wait_for_intercept_ready()
#
#        Check if Intercept module is ready.
#
#        :param max_retries: Number of retries to check if sport
#                            intercept module is ready. Defaults to 20
#        :type max_retries: Integer
#        :param min_interval: Min seconds between polls.
#                             Defaults to 3 seconds
#        :type min_interval: Integer.
#
#        :return result: True if intercept module is ready else False.
#        """
#        result = any(x['intercept module ready'] for x in polling.do_poll(
#            self.model.show_sport_intercept,
#            max_poll_retries=max_retries,
#            min_poll_interval=min_interval))
#        return result
