from odoo import models, fields, api

class PurchaseAdvancePayment(models.TransientModel):
    _name = 'purchase.advance.payment'
    _description = 'Purchase Advance Payment'

    journal_id = fields.Many2one('account.journal', string="Payment Journal", required=True,
                                 domain="[('type', 'in', ['bank', 'cash'])]")
    payment_status = fields.Selection([
        ('draft', 'Draft'),
        ('in_process', 'In Process')
    ], default='draft', required=True)

    amount = fields.Float(string="Payment Amount", required=True)
    

    partner_id = fields.Many2one('res.partner')
    purchase_id = fields.Many2one('purchase.order')
    
    

    def create_advance_payment(self):
        payment_vals = {
            'date': fields.Date.today(),
            'name' : self.id,
            'journal_id': self.journal_id.id,
            'partner_id' : self.partner_id.id,
            'amount': self.amount,
            'state': self.payment_status,
            'purchase_id': self.purchase_id.id, 

        }

        self.env['account.payment'].create(payment_vals)

       

        return {'type': 'ir.actions.act_window_close'}
    













# active_id = self.env.context.get('active_id')
#         order = self.env['sale.order'].browse(active_id)

#         if order.state in ['sale', 'draft', 'sent']:
#             order.state = 'cancel'
#             if self.send_email:
#                 template = self.env.ref('your_module_name.email_template_cancel_order')
#                 template.send_mail(order.id, force_send=True)
