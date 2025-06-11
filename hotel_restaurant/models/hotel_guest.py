from odoo import api, models, fields

class HotelGuest(models.Model):
    _inherit = "hotel.guest"

    restaurant_order_ids = fields.One2many("hotel.restaurant", "guest_id", string="Restaurant Orders")
