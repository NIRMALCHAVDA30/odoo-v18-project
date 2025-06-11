from odoo import api, models, fields

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_open_advance_payment_wizard(self):
        return {
            'name': 'Advance Payment',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.advance.payment',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_purchase_id': self.id,
                'default_partner_id': self.partner_id.id,
            }
        }
    
    #State button
    advance_payment_count = fields.Integer(compute="_compute_advance_payment_count")

    def _compute_advance_payment_count(self):
        for record in self:
            record.advance_payment_count = self.env['account.payment'].search_count([('purchase_id', '=', record.id)])

    def action_view_advance_payments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Advance Payments',
            'res_model': 'account.payment',
            'view_mode': 'list,form',
            'domain': [('purchase_id', '=', self.id)],
            'context': {'default_purchase_id': self.id, 'default_partner_id': self.partner_id.id},
        }
