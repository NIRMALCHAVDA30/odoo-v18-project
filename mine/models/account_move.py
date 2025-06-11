from odoo import models, fields, api
from datetime import date, timedelta

class Accountmove(models.Model):
    _inherit = 'account.move'

    #task 8: Return invoices that were validated but not paid.
    def invoice_validated(self):
        invoice = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '!=', 'paid'),
        ])
        print("\n\n\n--------->", invoice)
        # return invoice
    
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', invoice.ids)],
        }
    

    # Task: Check if a partner has an unpaid invoice older than 60 days.
    sixty_days_ago = date.today() - timedelta(days=60)
    print("\n\n\n\n-----------++++>", sixty_days_ago)

    def unpaid_invoice(self):
        unpaid = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('move_type', '=', 'out_invoice'),
            ('payment_state', '!=', 'paid'),
            ('invoice_date_due', '<=', self.sixty_days_ago)
        ])

        partners = unpaid.mapped('partner_id')
        print("\n\n\n--------->", partners.ids)



