from odoo import models, fields,api

class ShippingRoute(models.Model):
    _name = 'shipping.route'
    _description = 'Shipping Route'
    _rec_name = 'route_name'


    route_name = fields.Char(compute="_compute_route_name" , store=True)

    source_city = fields.Char(required=True)
    destination_city = fields.Char(required=True)
    distance_km = fields.Float(string="Distance (KM)")
    route_line_ids = fields.One2many('route.line', 'route_id')


    @api.depends("source_city" ,"destination_city")
    def _compute_route_name(self):
        for record in self:
            record.route_name = f"{record.source_city} to {record.destination_city}"