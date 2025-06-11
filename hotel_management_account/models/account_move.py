from odoo import models, api,  fields
from odoo import Command

class AccountMove(models.Model):
    _inherit = "account.move"

    hotel_id = fields.Many2one("hotel.management", string="Hotel Name")
    guest_id = fields.Many2one("guest")