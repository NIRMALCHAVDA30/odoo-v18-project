from odoo import models, fields, api

class HotelRestaurantLunchOrder(models.Model):
    _inherit = "lunch.order"

    guest_id = fields.Many2one("hotel.guest")
    room_id = fields.Many2one("hotel.room")
    order_history_ids = fields.One2many("lunch.order.history", "order_id", string="Order History")

    @api.model
    def create(self, vals):
        order = super().create(vals)
        self.env["lunch.order.history"].create({
            "order_id": order.id,
            "state": "placed",
            "description": f"Order created for Guest: {order.guest_id.name}"
        })
        return order
