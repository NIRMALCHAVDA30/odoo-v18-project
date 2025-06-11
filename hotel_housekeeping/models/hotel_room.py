from odoo import api, models, fields


class HotelRoom(models.Model):
    _inherit = "hotel.room"

    housekeeping_ids = fields.One2many("hotel.housekeeping", "room_id", string="Housekeeping")

    