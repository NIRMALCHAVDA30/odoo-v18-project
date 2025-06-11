from odoo import models, api, fields 
from odoo.exceptions import UserError 
from datetime import date, timedelta


class ShippingRoute(models.Model):
    _name = 'shipping.route'
    
    name = fields.Char(compute="_compute_name_details")
    source_city = fields.Char("Location")
    destination_city = fields.Char("Destination city")
    distance_km = fields.Float("Distance between cities")
    route_line_ids = fields.One2many("route.line","route_id")
    
    @api.depends('source_city','destination_city')
    def _compute_name_details(self):
        for record in self:
            if record.source_city and record.destination_city:
                record.name = f"{record.source_city} To {record.destination_city}"
            else:
                record.name = ''
