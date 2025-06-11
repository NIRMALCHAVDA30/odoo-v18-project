from odoo import models, api, fields # type: ignore
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    booking_id = fields.Many2one("courier.booking")