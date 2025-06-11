from odoo import models, fields, api

class HotelRestaurant(models.Model):
    _name = "hotel.restaurant"
    _description = "Hotel Restaurant "
    _rec_name = "room_id"
    
    # guest_id = fields.Many2one("hotel.guest", string="Guest", required=True)
    guest_id = fields.Many2one("res.partner", string="Guest",domain=[('is_guest', '=', True)], required=True)
    room_id = fields.Many2one("hotel.room", string="Room")
    order_date = fields.Datetime("Order Date", default=fields.Datetime.now , readonly=True)
    
    order = fields.Many2many("restaurant.order",string="Order Items")
    total_amount = fields.Float("Total Amount", compute="_compute_total", store=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("confirmed", "Confirmed"),
    ], default="draft", string="Status")

    @api.depends("order.total_price")
    def _compute_total(self):
        for record in self:
            record.total_amount = sum(record.order.mapped("total_price"))

    def action_confirm(self):
        self.state = "confirmed"
