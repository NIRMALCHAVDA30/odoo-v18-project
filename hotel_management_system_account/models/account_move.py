from odoo import models, api,  fields
from odoo import Command

class AccountMove(models.Model):
    _inherit = "account.move"

    hotel_id = fields.Many2one("hotel.management", string="Hotel Name")
    guest_id = fields.Many2one("hotel.guest")

    def action_post(self):
        """Override invoice validation to update reservation payment status"""
        result = super().action_post()
        for invoice in self:
            if invoice.move_type == "out_invoice" and invoice.state == "posted":
                reservation = self.env["hotel.reservation"].search([("invoice_id", "=", invoice.id)], limit=1)
                print("\n\n\n\n\n\n\n\n......iddddd....\n\n\n\n\n\n\n\n\n", invoice.id)
                print("\n\n  ", "invoice_id")
                if reservation:
                    reservation.payment_status = "paid"
        return result
    
