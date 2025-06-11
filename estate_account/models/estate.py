from odoo import models, api
from odoo.exceptions import  ValidationError
from odoo import Command

class Estate(models.Model):
    _inherit = "estate.property"

    
    # def action_sold(self):
    #     journal = self.env["account.journal"].search([('type','=','purchase')], limit=1)
    #     print(".......JOURNAL...", journal)
    #     account = self.env["account.move"].create({
    #          'journal_id':journal.id,
    #          'move_type':'in_invoice',
    #          'partner_id':self.buyer_id.id
            
    #     })
    #     print("\n\n\n===========account", account)
    #     return super().action_sold()  #in super to the 2 arg pass class name and self but this not complousary


    def action_sold(self):
        print("===============Action sold called")
        super().action_sold()
        journal = self.env["account.journal"].search([('type','=','sale')], limit=1)
        invoice = self.env['account.move'].create(
            {
            'journal_id':journal.id,
            'partner_id': self.buyer_id.id, 
            'move_type': 'out_invoice',
            "invoice_line_ids": [
                    Command.create({
                        "name" : "Selling Price",
                        "quantity" : 1,
                        "price_unit" : self.selling_price,
                    }),
                    # Command.create({
                    #     "name" : "6% of the Selling Price",
                    #     "quantity" : 1,
                    #     "price_unit" : self.selling_price * 0.06,
                    # }),
                    Command.create({
                    "name": "Administrative Fees",
                    "quantity": 1,
                    "price_unit": 100.00,
                    }),
                ],  
        }
        )

        return {
            "type": "ir.actions.act_window",
            "name": "Invoice",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": invoice.id,
            "target": "current",
        }
