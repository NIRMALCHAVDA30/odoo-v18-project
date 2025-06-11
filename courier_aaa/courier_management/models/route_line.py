from odoo import models, api, fields 
from odoo.exceptions import UserError 
from datetime import date, timedelta


class RouteLine(models.Model):
    _name = 'route.line'
    _rec_name = "mode_id"
    
    route_id = fields.Many2one("shipping.route")
    mode_id = fields.Many2one("shipping.mode")
    cost_per_kg = fields.Float()
    estimated_days = fields.Integer()
    is_active = fields.Boolean()