from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools import format_date

class OrneInterimMission(models.Model):
    _name = 'orne_interim.mission'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Demande de mission d\'intérim'

    _LOCKED_FIELDS_FROM_IN_PROGRESS = {
        'partner_id',
        'mission_type',
        'expected_workers',
        'description',
        'date_start',
        'date_end',
    }
    _LOCKED_FIELDS_IN_TERMINAL_STATES = {'hourly_rate'}
    _LOCKED_FIELD_LABELS = {
        'partner_id': 'Client',
        'mission_type': 'Type de mission',
        'expected_workers': 'Nombre de personnes',
        'description': 'Description',
        'date_start': 'Date de début',
        'date_end': 'Date de fin',
        'hourly_rate': 'Taux horaire',
    }
    
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

        if not self.env.context.get('bypass_mission_lock'):
            updated_fields = set(vals)
            for rec in self:
                locked_fields = set()
                if rec.state in ['in_progress', 'closed', 'invoiced', 'cancelled']:
                    locked_fields |= self._LOCKED_FIELDS_FROM_IN_PROGRESS
                if rec.state in ['invoiced', 'cancelled']:
                    locked_fields |= self._LOCKED_FIELDS_IN_TERMINAL_STATES

                blocked_fields = sorted(updated_fields & locked_fields)
                if blocked_fields:
                    labels = ', '.join(self._LOCKED_FIELD_LABELS[field_name] for field_name in blocked_fields)
                    raise UserError(
                        "Mission %s : les champs suivants sont verrouillés dans cet état : %s."
                        % (rec._get_state_label(), labels)
                    )
        return super(OrneInterimMission, self).write(vals)

    def _normalize_description(self):
        self.ensure_one()
        return ' '.join((self.description or '').split())

    def _format_mission_date(self, date_value):
        return format_date(self.env, date_value) if date_value else "non renseignée"

    def _get_state_label(self):
        self.ensure_one()
        return dict(self._fields['state'].selection).get(self.state, self.state)

    def _check_qualification_readiness(self):
        self.ensure_one()
        if not self.partner_id:
            raise UserError("Renseignez le client avant de qualifier la mission.")
        if not self.date_start or not self.date_end:
            raise UserError("Renseignez les dates de début et de fin avant de qualifier la mission.")
        if self.date_end < self.date_start:
            raise UserError("La date de fin doit être postérieure ou égale à la date de début.")
        if self.expected_workers < 1:
            raise UserError("Le nombre de personnes doit être au moins de 1.")
        if len(self._normalize_description()) < 5:
            raise UserError("Ajoutez une description plus précise avant de qualifier la mission.")


    # Méthodes de transition du workflow
    def action_qualify(self):
        for rec in self:
            if rec.state != 'received':
                raise UserError("Seules les missions à l'état 'Reçue' peuvent être qualifiées.")
            rec._check_qualification_readiness()
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
            if not rec.date_start or not rec.date_end:
                raise UserError("Renseignez les dates de début et de fin avant de démarrer la mission.")
            today = fields.Date.context_today(self)
            if today < rec.date_start:
                raise UserError(
                    "Démarrage impossible avant le %s." % rec._format_mission_date(rec.date_start)
                )
            if today > rec.date_end:
                raise UserError(
                    "Démarrage impossible : la mission était prévue jusqu'au %s."
                    % rec._format_mission_date(rec.date_end)
                )
            rec.with_context(allow_state_write=True).write({'state': 'in_progress'})

    def action_close(self):
        for rec in self:
            if rec.state != 'in_progress':
                raise UserError("Seules les missions à l'état 'En cours' peuvent être clôturées.")
            if not rec.date_end:
                raise UserError("La date de fin est requise pour clôturer la mission.")
            today = fields.Date.context_today(self)
            if today < rec.date_end:
                raise UserError(
                    "Impossible de clôturer une mission qui n'est pas encore terminée dans le temps. "
                    "Date de fin prévue : %s." % rec._format_mission_date(rec.date_end)
                )
            rec.with_context(allow_state_write=True).write({'state': 'closed'})

    def action_invoice_mark(self):
        for rec in self:
            if rec.state != 'closed':
                raise UserError("Seules les missions à l'état 'Clôturée' peuvent être marquées comme facturées.")
            if not rec.date_end:
                raise UserError("La date de fin est requise pour facturer la mission.")
            today = fields.Date.context_today(self)
            if today < rec.date_end:
                raise UserError(
                    "Impossible de facturer une mission qui n'est pas encore terminée. "
                    "Date de fin prévue : %s." % rec._format_mission_date(rec.date_end)
                )
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
