from odoo import models, fields, api

class Accountmove(models.Model):
    _inherit = 'account.move'

    #task 8
    def invoice_validated(self):
        invoice = self.env['account.move'].search([
            ('state', '=', 'posted'),
            ('payment_state', '!=', 'paid'),
        ])
        print("\n\n\n--------->", invoice)
        return invoice