# C:\Users\heric\odoo-dev-projects\addons\real_estate_ads\models\property_offer.py
from odoo import fields, models, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')], string="Status")
    partner_id = fields.Many2one('res.partner', string="Customer")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer(string="Validity")
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
    creation_date = fields.Date(string="Create Date")

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    def _inverse_deadline(self):
        for rec in self:
            if rec.creation_date and rec.deadline:
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    @api.model_create_multi
    def create(self, vals):
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()

            # Vérifie si le prix est supérieur à 10 000 euros
            if rec.get('price', 0) < 10000:
                raise ValidationError("Price must be greater than 10,000 euros")
        return super(PropertyOffer, self).create(vals)

    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline <= rec.creation_date:
                raise models.ValidationError("Deadline can not be before creation date")

    def write(self, vals):
        for rec in self:
            if rec.deadline and rec.deadline < fields.Date.today():
                raise ValidationError("Deadline can not be before creation date")
        return super(PropertyOffer, self).write(vals)
    
    def write(self, vals):
        print(self.env.cr)
        print(self.env.uid)
        print(self.env.context)
        res_partner_ids = self.env['res.partner'].search([
            ('is_company', '=', True),
        ]).filtered(lambda r: r.phone == '123456789')
        return super(PropertyOffer, self).write(vals)
    