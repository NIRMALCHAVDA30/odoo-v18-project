from odoo import models, fields, api

class SaleCancelWizard(models.TransientModel):
    _name = 'sale.cancel.wizard'
    _description = 'Cancel Sale Order Wizard'

    reason = fields.Char(required=True)
    send_email = fields.Boolean(string='Send Email to Customer', default=True)
    reason_details = fields.Text()

    def action_cancel_order(self):
        pass

        return {'type': 'ir.actions.act_window_close'}
