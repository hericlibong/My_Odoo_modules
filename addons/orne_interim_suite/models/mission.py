from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class OrneInterimMission(models.Model):
    _name = 'orne_interim.mission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Demande de mission d\'intérim'
    
    # Champs de base
    name = fields.Char(string='Référence', required=True, readonly=True, default='/')
    partner_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        help='Entreprise cliente',
        tracking=True,
    )
    
    # Type de mission
    mission_type = fields.Selection([
        ('btp', 'BTP'),
        ('nettoyage', 'Nettoyage/Tertiaire')
    ], string='Type de mission', required=True, default='btp', tracking=True)
    
    # Période
    date_start = fields.Date(string='Date de début', required=True, tracking=True)
    date_end = fields.Date(string='Date de fin', required=True, tracking=True)
    
    # Détails de la demande
    expected_workers = fields.Integer(string='Nombre de personnes', required=True, default=1, tracking=True)
    hourly_rate = fields.Float(
        string='Taux horaire',
        digits=(16, 2),
        help='Taux horaire facturé au client',
        groups="orne_interim_suite.group_orne_interim_manager,orne_interim_suite.group_orne_interim_admin",
        tracking=True,
    )
    description = fields.Text(string='Description des besoins')
    
    # Workflow
    state = fields.Selection([
        ('received', 'Reçue'),
        ('qualified', 'Qualifiée'),
        ('proposed', 'Proposée'),
        ('confirmed', 'Confirmée'),
        ('in_progress', 'En cours'),
        ('closed', 'Clôturée'),
        ('invoiced', 'Facturée'),
        ('cancelled', 'Annulée')
    ], string='État', default='received', required=True, tracking=True)
    
    # Annulation
    cancel_reason = fields.Text(string="Raison d'annulation")
    
    # Champs calculés
    duration_days = fields.Integer(string='Durée (jours)', compute='_compute_duration', store=True)
    
    @api.depends('date_start', 'date_end')
    def _compute_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                record.duration_days = (record.date_end - record.date_start).days + 1  # Inclusif
            else:
                record.duration_days = 0
    
    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end and record.date_end < record.date_start:
                raise ValidationError("La date de fin doit être postérieure ou égale à la date de début.")

    # Séquence automatique (compatible batch)
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', '/') == '/':
                vals['name'] = self.env['ir.sequence'].next_by_code('orne.interim.mission') or '/'
        return super(OrneInterimMission, self).create(vals_list)

    def write(self, vals):
        # Protection contre les changements d'état manuels
        if 'state' in vals and not self.env.context.get('allow_state_write'):
            raise UserError("Changement d’état manuel non autorisé. Veuillez utiliser les boutons du workflow.")
        return super(OrneInterimMission, self).write(vals)


    # Méthodes de transition du workflow
    def action_qualify(self):
        for rec in self:
            if rec.state != 'received':
                raise UserError("Seules les missions à l'état 'Reçue' peuvent être qualifiées.")
            if not rec.partner_id:
                raise UserError("Le client est obligatoire pour qualifier la mission.")
            if not rec.date_start or not rec.date_end:
                raise UserError("Les dates de début et de fin sont obligatoires.")
            if rec.date_end < rec.date_start:
                raise UserError("La date de fin doit être postérieure à la date de début.")
            if rec.expected_workers < 1:
                raise UserError("Le nombre de personnes doit être au moins 1.")
            rec.with_context(allow_state_write=True).write({'state': 'qualified'})

    def action_propose(self):
        for rec in self:
            if rec.state != 'qualified':
                raise UserError("Seules les missions à l'état 'Qualifiée' peuvent être proposées.")
            rec.with_context(allow_state_write=True).write({'state': 'proposed'})

    def action_confirm(self):
        for rec in self:
            if rec.state != 'proposed':
                raise UserError("Seules les missions à l'état 'Proposée' peuvent être confirmées.")
            rec.with_context(allow_state_write=True).write({'state': 'confirmed'})

    def action_start(self):
        for rec in self:
            if rec.state != 'confirmed':
                raise UserError("Seules les missions à l'état 'Confirmée' peuvent être démarrées.")
            today = fields.Date.context_today(self)
            if today > rec.date_end:
                raise UserError("On ne peut pas démarrer une mission dont la date de fin est déjà dépassée.")
            rec.with_context(allow_state_write=True).write({'state': 'in_progress'})

    def action_close(self):
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError("Seules les missions à l'état 'En cours' peuvent être clôturées.")
            today = fields.Date.context_today(self)
            if today < rec.date_end:
                raise UserError("Impossible de clôturer une mission qui n'est pas encore terminée dans le temps.")
            rec.with_context(allow_state_write=True).write({'state': 'closed'})

    def action_invoice_mark(self):
        for rec in self:
            if rec.state != 'closed':
                raise UserError("Seules les missions à l'état 'Clôturée' peuvent être marquées comme facturées.")
            today = fields.Date.context_today(self)
            if today < rec.date_end:
                raise UserError("Impossible de facturer une mission qui n'est pas encore terminée dans le temps.")
            rec.with_context(allow_state_write=True).write({'state': 'invoiced'})

    def action_back_step(self):
        """Revenir d'un cran dans le workflow"""
        back_mapping = {
            'qualified': 'received',
            'proposed': 'qualified',
            'confirmed': 'proposed',
            'in_progress': 'confirmed',
            'closed': 'in_progress'
        }
        for rec in self:
            if rec.state in ['received', 'cancelled', 'invoiced']:
                raise UserError("Retour impossible depuis l'état '{}'.".format(rec.state))
            
            new_state = back_mapping.get(rec.state)
            if new_state:
                rec.with_context(allow_state_write=True).write({'state': new_state})
            else:
                raise UserError("Transition de retour non définie pour l'état '{}'.".format(rec.state))

    def action_cancel(self):
        """Annuler la mission"""
        for rec in self:
            if rec.state == 'invoiced':
                raise UserError("Mission facturée : annulation interdite.")
            rec.with_context(allow_state_write=True).write({'state': 'cancelled'})

    def action_reactivate(self):
        """Réactiver une mission annulée"""
        for rec in self:
            if rec.state != 'cancelled':
                raise UserError("Seules les missions annulées peuvent être réactivées.")
            rec.with_context(allow_state_write=True).write({
                'state': 'received',
                'cancel_reason': False,
            })
