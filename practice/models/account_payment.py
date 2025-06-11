from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    purchase_id = fields.Many2one('purchase.order')
