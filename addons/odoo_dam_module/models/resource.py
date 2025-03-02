from odoo import models, fields, api


class Resource(models.Model):
    _name = 'dam.resource'
    _description = 'Digital Asset Management Resource'


    name = fields.Char(string='Name', required=True, help='Name of the resource')
    file = fields.Binary(string='File', required=True, help='File of the resource')
    type = fields.Selection([
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('document', 'Document'),
        ('other', 'Other')
    ], string='Type', required=True, help='Type of the resource')
    description = fields.Text(string='Description', help='Description of the resource')
    project_id = fields.Many2one('project.project', string='Project', help='Project the resource belongs to')
    is_image = fields.Boolean(string='Is Image', compute='_compute_is_image', store=True)

    @api.depends('type')
    def _compute_is_image(self):
        for record in self:
            record.is_image = record.type == 'image'

    @api.model
    def create(self, vals):
        record = super(Resource, self).create(vals)
        self.env['dam.resource.log'].create({
            'resource_id': record.id,
            'action_type': 'create',
            'user_id': self.env.uid,
        })
        return record
    
    def write(self, vals):
        result = super(Resource, self).write(vals)
        for record in self:
            self.env['dam.resource.log'].create({
                'resource_id': record.id,
                'action_type': 'write',
                'user_id': self.env.uid,
            })
        return result
    
    def unlink(self):
        for record in self:
            self.env['dam.resource.log'].create({
                'resource_id': record.id,
                'action_type': 'unlink',
                'user_id': self.env.uid,
            })
        return super(Resource, self).unlink()
    
   



    


                    
