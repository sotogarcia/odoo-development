# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################


from openerp.tests.common import TransactionCase
from logging import getLogger


_logger = getLogger(__name__)


class ReportGroupsImplied(TransactionCase):
    """ This class contains the unit tests for 'report.groups.implied'.

        Tests:
          - all_implied: Checks all relationships between groups
    """

    def setUp(self):
        super(ReportGroupsImplied, self).setUp()

    def test_all_implied(self):
        """ Checks if results of the SQL query which serves as report source
            matches with the field implied_ids in all the res.groups

            Loads all groups in database
            By each group:
                - Searches for reports records which the same group_id
                - CHECKS: at least one record must exist
                - Gets a SORTED list with all report implied ids
                - CHECKS: group always must involve itself
                - Gets a SORTED UNREPEATED list with all ids in computed field:
                    res.groups->trans_implied_ids
                - Both sorted lists must be equals
        """

        group_obj = self.env['res.groups']
        group_set = group_obj.search([])

        report_obj = self.env['report.groups.implied']

        for group in group_set:
            report_set = report_obj.search([('group_id', '=', group.id)])

            self.assertTrue(
                report_set,
                'Report must contain all the groups'
            )

            rep_implied = [rep.implied_id for rep in report_set]
            rep_implied.sort()

            self.assertTrue(
                group.id in rep_implied,
                'Group should involve itself'
            )

            trans_implied = [imp.id for imp in group.trans_implied_ids]
            trans_implied.append(group.id)
            trans_implied = list(set(trans_implied))
            trans_implied.sort()

            self.assertListEqual(
                rep_implied,
                trans_implied,
                "Group %s not match" % str(group.id)
            )
