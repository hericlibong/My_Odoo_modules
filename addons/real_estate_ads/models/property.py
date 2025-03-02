# C:\Users\heric\odoo-dev-projects\addons\real_estate_ads\models\property.py
from odoo import models, fields, api

class Property(models.Model):
    _name = 'estate.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name', required=True)
    tag_ids = fields.Many2many('estate.property.tag', string='Property Tags')
    type_id = fields.Many2one('estate.property.type', string='Property Type')
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Data Availability')
    expected_price = fields.Float(string='Expected Price')
    best_offer = fields.Float(string='Best Offer')
    selling_price = fields.Float(string='Selling Price')
    bedrooms = fields.Integer()
    living_area = fields.Integer(string='Living Area(sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage', default=False)
    garden = fields.Boolean(string='Garden', default=False)
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation', default='north')
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Offers')
    sales_id = fields.Many2one('res.users', string='Salesman')
    buyer_id = fields.Many2one('res.partner', string='Buyer', domain=[('is_company', '=', True)])
    phone = fields.Char(string='Phone', related='buyer_id.phone')

    # 1 depends method
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    total_area = fields.Integer(string="Total Area", compute='_compute_total_area')

  

class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Real Estate Property Type'

    name = fields.Char(string='Name', required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Real Estate Property Tag'

    name = fields.Char(string='Name', required=True)
    
    