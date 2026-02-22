from odoo import models, fields, api

class OrneInterimMission(models.Model):
    _name = 'orne_interim.mission'
    _description = 'Demande de mission d\'intérim'
    
    # Champs de base
    name = fields.Char(string='Référence', required=True, readonly=True, default='/')
    partner_id = fields.Many2one('res.partner', string='Client', required=True, help='Entreprise cliente')
    
    # Type de mission
    mission_type = fields.Selection([
        ('btp', 'BTP'),
        ('nettoyage', 'Nettoyage/Tertiaire')
    ], string='Type de mission', required=True, default='btp')
    
    # Période
    date_start = fields.Date(string='Date de début', required=True)
    date_end = fields.Date(string='Date de fin', required=True)
    
    # Détails de la demande
    expected_workers = fields.Integer(string='Nombre de personnes', required=True, default=1)
    hourly_rate = fields.Float(string='Taux horaire', digits='Product Price', help='Taux horaire facturé au client')
    description = fields.Text(string='Description des besoins')
    
    # Workflow
    state = fields.Selection([
        ('received', 'Reçue'),
        ('qualified', 'Qualifiée'),
        ('proposed', 'Proposée'),
        ('confirmed', 'Confirmée'),
        ('in_progress', 'En cours'),
        ('closed', 'Clôturée'),
        ('invoiced', 'Facturée')
    ], string='État', default='received', required=True)
    
    # Détails de la demande
    hourly_rate = fields.Float(string='Taux horaire', digits=(16, 2), help='Taux horaire facturé au client')
    
    # Champs calculés
    duration_days = fields.Integer(string='Durée (jours)', compute='_compute_duration', store=True)
    
    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                delta = fields.Date.from_string(record.date_end) - fields.Date.from_string(record.date_start)
                record.duration_days = delta.days + 1  # Inclusif
            else:
                record.duration_days = 0
    
    # Séquence automatique (compatible batch)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('orne.interim.mission') or '/'
        return super(OrneInterimMission, self).create(vals_list)