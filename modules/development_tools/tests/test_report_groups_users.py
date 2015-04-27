# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp.tests.common import TransactionCase
from logging import getLogger


_logger = getLogger(__name__)


class ReportGroupsUsers(TransactionCase):
    """ This class contains the unit tests for 'report.groups.users'.

        Tests:
          - all_groups: checks report relationships between users and groups
    """

    def setUp(self):
        super(ReportGroupsUsers, self).setUp()

    def test_all_groups(self):
        """ Checks all report relationships between users and groups

            1. Loads all report.groups.users in database
            2. By each report:
                - CHECKS a single match with report.groups.implied
                - Loads implied group information
                - Loads the user information
                - CHECKS both are empty or user belongs to implied group

            NOTE:
                - report.groups.implied has its own unittest and it is executed
                before, here is assumed this test has finished with success.
        """

        report_domain = []
        report_obj = self.env['report.groups.users']
        report_set = report_obj.search(report_domain)

        for report in report_set:
            uid = report.user_id
            gid = report.implied_id

            implied_rep_domain = [
                ('group_id', '=', report.group_id),
                ('implied_id', '=', report.implied_id)
            ]
            implied_rep_obj = self.env['report.groups.implied']
            implied_rep_set = implied_rep_obj.search(implied_rep_domain)

            msg = ('It should be one match with `report.groups.implied` '
                   '(group_id: {}, implied_id: {}), but result have been {}')
            self.assertTrue(
                len(implied_rep_set) == 1,
                msg.format(
                    report.group_id,
                    report.implied_id,
                    len(implied_rep_set)
                )
            )

            group_domain = [('id', '=', gid)]
            group_obj = self.env['res.groups']
            group_set = group_obj.search(group_domain)

            user_domain = [('id', '=', uid)]
            user_obj = self.env['res.users']
            user_set = user_obj.search(user_domain)

            assert len(group_set) == 1 and len(user_set) <= 1, \
                'Oh, oh!, this is not possible!'

            if not group_set.users:
                msg = 'Group {} has not users but there is one ({}) in report'
                self.assertFalse(
                    user_set,
                    msg.format(gid, uid)
                )
            else:
                msg = 'Group {} has users ({}) but there is one in report'
                self.assertTrue(
                    user_set,
                    msg.format(gid, group_set.users)
                )

                msg = 'User {} not belongs to {} but report shows relationship'
                self.assertTrue(
                    user_set in group_set.users,
                    msg.format(uid, gid)
                )
