# -*- coding: utf-8 -*-

from openerp import models, fields
import datetime

class Sample(models.Model):
    _name = 'odoo_module_scaffolding.sample'
    _description = 'Basic model scaffolding'

    # sample = fields.Char(
    #   string="Sample name",           # Optional label of the field
    #   compute="_compute_name_custom", # Transform the fields in computed fields
    #   store=True,                     # If computed it will store the result
    #   select=True,                    # Force index on field
    #   readonly=True,                  # Field will be readonly in views
    #   inverse="_write_name"           # On update trigger
    #   required=True,                  # Mandatory field
    #   translate=True,                 # Translation enable
    #   help=’blabla’,                  # Help tooltip text
    #   company_dependent=True,         # Transform columns to ir.property
    #   search=’_search_function’       # Custom search function mainly used with compute
    # )

    abool = fields.Boolean(string='Boolean sample', default=True)
    achar = fields.Char(string='Char sample', default='Char')
    atext = fields.Text(string='Text caption', default='Text')
    anhtml = fields.Html(string='Html caption', default='<html><body>HTML</body></html>')
    anint = fields.Integer(string='Integer caption', default=0)
    #afloat = fields.Float(digits=(20, 2), string='Float caption', default=0.0)
    adate = fields.Date(string='Date caption', default=datetime.date.today())
    adatetime = fields.Datetime(string='Datetime caption', default=datetime.datetime.now())
    abin = fields.Binary(string='Binary caption')
    aselection = fields.Selection(string='Selection caption', selection=[('F', 'Female'), ('M', 'Male')])
    #aref = fields.Reference([(’model_name’, ’String’)])
    #arel_id_m2o = fields.Many2one(’res.users’)
    #arel_ids_o2m = fields.One2many(’res.users’, ’rel_id’)
    #arel_ids_m2m = fields.Many2many(’res.users’)
   
