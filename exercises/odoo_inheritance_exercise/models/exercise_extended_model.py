from openerp import models, fields


class ExerciseExtendedModel(models.Model):
    """ Model which extends parent funcionality with a new field

    Fields:
      middle_name (Char): Non required last name.
      last_name (Char): Non required last name.

    """

    _inherit = 'exercise.base.model'
    _description = u'Model which extends parent funcionality with a new field'

    _order = "name ASC, middle_name ASC, last_name ASC"

    middle_name = fields.Char(
        string='Middle name',
        required=False,
        readonly=False,
        default=None,
        help='Non required second name',
        size=50,
        translate=True
    )

    last_name = fields.Char(
        string='Last name',
        required=False,
        readonly=False,
        default=None,
        help='Non required third name',
        size=50,
        translate=True
    )
