from openerp import models, fields


class ExerciseBaseModel(models.Model):
    """ Model which will be parent of the all others.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'exercise.base.model'
    _inherit = ['mail.thread']
    _description = u'Model which will be parent of the all others'

    _rec_name = 'name'
    _order = "name DESC"

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Human readable name',
        size=50,
        translate=True,
        track_visibility='onchange',
    )
