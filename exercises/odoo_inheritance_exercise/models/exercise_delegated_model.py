from openerp import models, fields


class ExerciseDelegatedModel(models.Model):
    """ Delegated model which contains an instance of exercise.delegated.model

    Fields:
      color (Char): color attribute for the specific variant

    """

    _name = 'exercise.delegated.model'
    _inherit = ['mail.thread']
    _inherits = _inherits = {
        'exercise.inherited.model': 'inherited_id',
    }
    _description = ('Delegated model which contains an instance of '
                    'exercise.delegated.model')

    _rec_name = 'name'
    _order = "name ASC"

    inherited_id = fields.Many2one(
        string='Parent object',
        required=True,
        readonly=False,
        help="Relationship with the parent model",
        comodel_name='exercise.inherited.model',
        ondelete='cascade',
    )

    color = fields.Selection(
        string='Color',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help="Variant specific attribute",
        selection=[
            ('R', 'Red'),
            ('O', 'Orange'),
            ('Y', 'Yellow'),
            ('G', 'Green'),
            ('B', 'Blue'),
            ('I', 'Indigo'),
            ('V', 'Violet')
        ]
    )
