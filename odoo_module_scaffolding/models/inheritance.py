# -*- coding: utf-8 -*-

from openerp import models, fields

class InheritanceBase(models.Model):
    _name = 'odoo_module_scaffolding.inheritance.base'
    _description = 'Odoo basic inheritance base class'

    source_id = fields.Many2one (
        'crm.tracking.source',
        string='Source',
    )

    coupon_date = fields.Char (
        string='Request date',
        required=False
    )

    training_id = fields.Many2one(
        'product.template',
        string='Training',
    )

class InheritanceDerived(models.Model):
    _name = 'odoo_module_scaffolding.inheritance.derived'
    _inherit = 'odoo_module_scaffolding.inheritance.base'
    _description = 'Odoo basic inheritance derived class'

    name = fields.Char(
        string='Name'
    )
