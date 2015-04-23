from openerp import models, fields, api


class ExerciseInheritedModel(models.Model):
    """ Model that inherits from base model but has its own name.

    Fields:
      brand (Char): brand for a product.

    """

    _name = 'exercise.inherited.model'
    _inherit = 'exercise.base.model'
    _description = u'Model that inherits from base model but has its own name'

    _rec_name = 'name'
    _order = "name DESC"

    purchase_price = fields.Float(
        string='Purchase price',
        required=True,
        readonly=False,
        default=0.0,
        help='Price of the product when you purchase it'
    )

    @api.one
    @api.onchange('purchase_price')
    def _onchange_purchase_price(self):
        self.profit_margin = self.sale_price - self.purchase_price

    sale_price = fields.Float(
        string='Sale price',
        required=True,
        readonly=False,
        default=0.0,
        help='Price of the item when you sale it'
    )

    @api.one
    @api.onchange('sale_price')
    def _onchange_sale_price(self):
        self.profit_margin = self.sale_price - self.purchase_price

    profit_margin = fields.Float(
        string='Profit margin',
        required=True,
        readonly=True,
        default=0.0,
        help='Price difference between purchase price and sale price',
        compute=lambda self: self._compute_profit_margin()
    )

    @api.multi
    @api.depends('sale_price', 'purchase_price')
    def _compute_profit_margin(self):
        for record in self:
            record.profit_margin = record.sale_price - record.purchase_price

    delegated_ids = fields.One2many(
        string='Delegated submodels',
        required=False,
        readonly=False,
        help='Show all delegated model items which this inside',
        comodel_name='exercise.delegated.model',
        inverse_name='inherited_id'
    )
