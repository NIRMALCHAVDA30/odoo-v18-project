from odoo import models, fields, api
from datetime import date, timedelta

class AccountMove(models.Model):
    _inherit = 'account.move'

    
    sixty_days_ago = date.today() - timedelta(days=60)

    def unpaid_invoice(self):
        unpaid = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid'),
            ('invoice_date_due', '<=', self.sixty_days_ago)
        ])

        partners = unpaid.mapped('partner_id')
        print("\n\n\n--------->", partners.name)