from odoo import models, fields

class ShippingSuggestion(models.Model):
    _name = 'shipping.suggestion'
    _description = 'Shipping Suggestion'

    booking_id = fields.Many2one('courier.booking')
    route_line_id = fields.Many2one('route.line', required=True)
    estimated_days = fields.Integer()
    estimated_cost = fields.Monetary()
    suggestion_type = fields.Selection([
        ('cheapest', 'Cheapest'),
        ('fastest', 'Fastest'),
        ('balanced', 'Balanced')
    ], required=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self.env.company.currency_id)
    

    #Choose Button
    def action_choose_route(self):
        for record in self:
            booking = record.booking_id
            route_line = record.route_line_id

            if booking and route_line:
                booking.cost = booking.weight * record.estimated_cost
                booking.selected_mode_id = route_line.mode_id.id
                booking.route_id = route_line.route_id.id
                booking.price_per_estimeted_cost = record.estimated_cost
                booking.delivery_estimate = record.estimated_days
