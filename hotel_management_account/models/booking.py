from odoo import models, api, fields, _
from odoo import Command


class Booking(models.Model):
    _inherit = "booking"

    def action_book_room(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

        invoice = self.env["account.move"].create(
            {
                "journal_id": journal.id,
                "partner_id": self.guest_id.id,
                "move_type": "out_invoice",
                "hotel_id": self.hotel_id.id,
                "guest_id": self.guest_id.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": self.room_type,
                            "quantity": 1,
                            "price_unit": self.total_price,
                        }
                    ),
                    Command.create(
                        {
                            "name": "GST",
                            "quantity": 1,
                            "price_unit": 100.00,
                        }
                    ),
                ],  
            }
        )

        # return super().action_book_room()
        return {
            "type": "ir.actions.act_window",
            "name": _("Customer Invoice"),
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": invoice.id,
            "target": "current",
        }
