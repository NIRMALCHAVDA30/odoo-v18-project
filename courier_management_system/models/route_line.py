from odoo import models, fields

class RouteLine(models.Model):
    _name = 'route.line'
    _description = 'Route Line'
    _rec_name = 'route_id'

    route_id = fields.Many2one('shipping.route', required=True)
    mode_id = fields.Many2one('shipping.mode', required=True)
    cost_per_kg = fields.Float(string="Cost Per Kg", required=True)
    estimated_days = fields.Integer()
    is_active = fields.Boolean(string="Active", default=True)