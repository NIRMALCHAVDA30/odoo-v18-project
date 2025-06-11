from odoo import models, api, fields, _
from odoo import Command


class CourierBooking(models.Model):
    _inherit = 'courier.booking'


    def action_create_invoice(self):
        super().action_create_invoice()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

        invoice = self.env["account.move"].create(
            {
                "journal_id": journal.id,
                "partner_id": self.sender_id.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.product_id.name,
                            "quantity": self.weight,
                            "price_unit": self.price_per_estimeted_cost,
                        }
                    ),
                ],  
            }
        )


        self.invoice_id = invoice


