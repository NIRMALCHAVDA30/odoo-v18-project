from odoo import models, fields

class HotelRestaurantLunchOrderHistory(models.Model):
    _name = "lunch.order.history"
    _description = "Track Restaurant Order History"

    order_id = fields.Many2one("lunch.order", string="Order", required=True)
    state = fields.Selection([
        ("placed", "Placed"),
        ("preparing", "Preparing"),
        ("delivered", "Delivered"),
        ("billed", "Billed"),
    ], string="Order Status", default="placed")
    description = fields.Text()
    timestamp = fields.Datetime(default=fields.Datetime.now)
