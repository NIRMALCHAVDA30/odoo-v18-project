from odoo import models, fields, api, _
from odoo import Command


class HotelBooking(models.Model):
    _inherit = "hotel.booking"

    def action_create_invoice(self):
        super().action_create_invoice()
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)

        partner = self.env['res.partner'].create({
        'name': self.guest_id.name,
        })

        invoice_lines = []
        for line in self.room_line_ids: 
            invoice_lines.append(Command.create({
                "name": line.room_id.room_type_id.name, 
                "quantity": line.booking_id.days,
                "price_unit": line.amount,
            }))

        # invoice_lines.append(Command.create({
        #     "name": "GST",
        #     "quantity": 1,
        #     "price_unit": 100.00, 
        # }))

        #restraunt order
        for record in self:
            invoice_lines.append(Command.create({
                "name": "Restraunt Order",
                "quantity": 1,
                "price_unit": record.total_order_price, 
            }))

        invoice = self.env["account.move"].create({
            "journal_id": journal.id,
            "partner_id": partner.id,
            "move_type": "out_invoice",
            "invoice_line_ids": invoice_lines,
        })

        # Link invoice to booking
        self.invoice_id = invoice.id

        return {
            "type": "ir.actions.act_window",
            "name": "Invoice",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": invoice.id,
            "target": "current",
        }

