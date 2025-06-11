from odoo import models, api,  fields
from odoo import Command

class SaleOrder(models.Model):
    _inherit = "sale.order"

    hotel_id = fields.Many2one("hotel.management", string="Hotel Name")
    room_id = fields.Many2one("hotel.room")