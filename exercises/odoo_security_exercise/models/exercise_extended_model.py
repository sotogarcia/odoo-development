from openerp import models, fields


class ExerciseExtendedModel(models.Model):
    """ Model which extends a model from another module

    Fields:
      treatment (Char): Treatment applicable to each person.

    """

    _inherit = 'exercise.base.model'
    _description = u'Model which extends a model from another module'

    treatment = fields.Selection(
        string='Treatment',
        required=False,
        readonly=True,
        help="Treatment applicable to each person",
        selection=[('mr', 'Mister'), ('mrs', 'Madam')]
    )
