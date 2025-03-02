from odoo import models, fields

class ResourceLog(models.Model):
    _name = 'dam.resource.log'
    _description = 'Log of Actions on Resources'
    _order = 'timestamp desc'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        readonly=True,
        help="User who performed the action."
    )
    resource_id = fields.Many2one(
        'dam.resource',
        string='Resource',
        required=False,
        readonly=True,
        ondelete='set null',
        help="Resource on which the action was performed."
    )
    action_type = fields.Selection(
        [
            ('create', 'Created'),
            ('write', 'Modified'),
            ('unlink', 'Deleted')
        ],
        string='Action Type',
        required=True,
        readonly=True,
        help="Type of action performed."
    )
    timestamp = fields.Datetime(
        string='Timestamp',
        default=fields.Datetime.now,
        readonly=True,
        help="Date and time of the action."
    )
    
