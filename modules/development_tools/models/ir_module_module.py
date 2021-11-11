# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
""" Module

This module contains the module an unique Odoo model which extends
base.ir.module.module existing model. Here will be added a boolean field
to check if this module is in developement.

Classes:
    Module: This is the unique model class in this module
    and extends base.ir.module.module

    Inside this class can be, in order, the following attributes and methods:
    * Entity fields with the full definition

"""


# pylint: disable=locally-disabled, E0401
from openerp import models, fields


# pylint: disable=locally-disabled, R0903
class Module(models.Model):
    """ This model is the representation of the odoo module

    Fields:
      developing (Boolean): Checked means record belongs to a module which
      is in development.
    """


    _name = 'ir.module.module'
    _description = u'Module'

    _inherit = ['ir.module.module']



    favourite = fields.Boolean(
        string='Developing',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check if this module is in development',
        oldname='developing'
    )
