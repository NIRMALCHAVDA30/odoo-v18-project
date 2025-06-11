from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    cancel_reason_id = fields.Many2one('sale.cancel.reason', string='Cancel Reason')

    def action_open_cancel_wizard(self):
        print("button was clicked", "\n\n\n\n")
        return {
            'name': 'Cancel Order',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.cancel.wizard',
            'view_mode': 'form',
            'target': 'new',
            # 'context': {
            #     'default_purchase_id': self.id,
            #     'default_partner_id': self.partner_id.id,
            # }
        }