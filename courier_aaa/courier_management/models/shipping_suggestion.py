from odoo import models, api, fields 
from odoo.exceptions import UserError 
from datetime import date, timedelta


class ShippingSuggestion(models.Model):
    _name = 'shipping.suggestion'
    
    booking_id = fields.Many2one("courier.booking")
    route_line_id = fields.Many2one("route.line")
    estimated_days = fields.Integer()
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 default=lambda self: self.env.user.company_id.currency_id.id)
    estimated_cost = fields.Monetary(currency_field='currency_id',string="Estimated Cost")
    suggestion_type = fields.Selection(
        selection = [('fastest','Fastest'),('balanced','Balanced'),('cheapest','Cheapest')])

    def action_choose_mode_btn(self):
        for rec in self:
            try:
                if rec.booking_id.is_chosen == False:
                    weight = float(rec.booking_id.weight or 0.0)
                    estimated_cost = float(rec.estimated_cost or 0.0)
                    rec.booking_id.cost = estimated_cost * weight
                    rec.booking_id.delivery_estimate = rec.estimated_days
                    rec.booking_id.selected_mode_id = rec.route_line_id.mode_id.id
                    rec.booking_id.per_kg_cost = rec.estimated_cost
                    rec.booking_id.is_chosen = True
                    rec.booking_id.is_flag = True
                else:
                    raise UserError("Already Plan is Choosed.")
            except ValueError:
                raise UserError("Enter a Weight in Number.")