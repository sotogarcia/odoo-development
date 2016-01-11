# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0212,E0611,C0103,R0903,C0111
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AtTestBuilderWizard(models.Model):
    """ Test builder wizard

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'at.test.builder.wizard'
    _description = u'Test builder wizard'

    _rec_name = 'name'
    _order = 'create_date DESC'

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Name which will be used to store the test',
        size=50,
        translate=True
    )

    main_questions = fields.Integer(
        string='Quesions',
        required=True,
        readonly=False,
        index=False,
        default=10,
        help='Number of questions needed to build a test'
    )

    extra_questions = fields.Integer(
        string='Extra questions',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help='Questions can be used when some of the main questions are invalid'
    )

    num_tests = fields.Integer(
        string='Number of tests',
        required=True,
        readonly=False,
        index=False,
        default=1,
        help='Number of test will be build'
    )

    num_answers = fields.Integer(
        string='Needed answers',
        required=True,
        readonly=False,
        index=False,
        default=4,
        help='Number of answers by each one of questions'
    )

    right_answers = fields.Selection(
        string='Right answers',
        required=True,
        readonly=False,
        index=False,
        default='one',
        help='Required number of right answers',
        selection=[('none', 'Allow none'), ('one', 'Require one'), ('multi', 'Allow multiple')]
    )

    random_answers = fields.Selection(
        string='Random answers',
        required=True,
        readonly=False,
        index=False,
        default='fill',
        help='Allow to use answers from other questions',
        selection=[('none', 'Never use'), ('fill', 'Fill as needed'), ('always', 'Always allowed')]
    )

    at_topic_ids = fields.Many2many(
        string='Topics',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_all_ids('at.topic'),
        help='Topics will be inluded or excluded from test',
        comodel_name='at.topic',
        #relation='at_topic_this_model_rel',
        #column1='at_topic_id',
        #column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    at_topic_exclude = fields.Boolean(
        string='Exclude selected topics',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=('The selected topics will be excluded from test. '
              'All other available topics will be included.')
    )

    at_category_ids = fields.Many2many(
        string='Categories',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_all_ids('at.category'),
        help='Categories will be inluded or excluded from test',
        comodel_name='at.category',
        # relation='at_category_this_model_rel',
        # column1='at_category_id',
        # column2='this_model_id',
        domain=lambda self: self._compute_at_category_ids_domain(),
        context={},
        limit=None
    )

    at_category_exclude = fields.Boolean(
        string='Exclude selected categories',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=('The selected categories will be excluded from test. '
              'All other available categories will be included.')
    )

    at_tag_ids = fields.Many2many(
        string='Tags',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_all_ids('at.tag'),
        help='Tags will be inluded or excluded from test',
        comodel_name='at.tag',
        # relation='at_tag_this_model_rel',
        # column1='at_tag_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    at_tag_exclude = fields.Boolean(
        string='Exclude selected tags',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=('The selected tags will be excluded from test. '
              'All other available tags will be included.')
    )

    at_level_ids = fields.Many2many(
        string='Levels',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_all_ids('at.level'),
        help='Levels will be inluded or excluded from test',
        comodel_name='at.level',
        # relation='at_category_this_model_rel',
        # column1='at_category_id',
        # column2='this_model_id',
        domain=[],
        context={},
        limit=None
    )

    at_level_exclude = fields.Boolean(
        string='Exclude selected levels',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help=('The selected levels will be excluded from test. '
              'All other available levels will be included.')
    )
    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    def _compute_at_category_ids_domain(self):
        """ Computes domain for at_category_ids, this should allow categories
        only in the selected topic.
        """

        id_list = self.at_topic_ids.at_category_ids.mapped('id')

        return [('id', 'in', tuple(id_list))]

    @api.model
    def _default_all_ids(self, model):
        model_domain = [('id', '>=', 1)]
        model_obj = self.env[model]
        return model_obj.search(model_domain).mapped('id')

    # --------------------------- ONCHANGE EVENTS -----------------------------

    @api.onchange('at_topic_ids')
    def _onchange_at_topid_ids(self):
        """ Updates domain form at_category_ids, this shoud allow categories
        only in the selected topic.
        """

        current_list = self.at_category_ids.mapped('id')
        topic_list = self.at_topic_ids.at_category_ids.mapped('id')

        self.at_category_ids = \
            [(6, 0, [val for val in current_list if val in topic_list])]

        return {
            'domain': {
                'at_category_ids': [('id', 'in', tuple(topic_list))]
            }
        }


