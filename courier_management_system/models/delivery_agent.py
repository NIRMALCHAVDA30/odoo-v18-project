from odoo import models, fields, api

class DeliveryAgent(models.Model):
    _name = 'delivery.agent'
    _description = 'Delivery Agent'

    name = fields.Char(string="Agent Name",compute="_compute_name", store=True)
    user_id = fields.Many2one('res.users', required=True)
    is_available = fields.Boolean(string="Available", default=True)


    @api.depends('user_id')
    def _compute_name(self):
        if self.user_id:
            self.name = self.user_id.name