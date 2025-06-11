from odoo import models, api, fields, _
from odoo import Command
from odoo.exceptions import ValidationError


class HotelInvoice(models.Model):
    _inherit = "hotel.reservation"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order", readonly=True)
    

    def action_book_room(self):
        super(HotelInvoice, self).action_book_room()

        product = self.env["product.product"].create({
                "name": self.hotel_id.name,
                "type": "service", 
                "list_price": self.total_price,
            })

        sale_order = self.env["sale.order"].create({
            "partner_id": self.guest_id.id,
            "hotel_id": self.hotel_id.id,
            "room_id": self.room_id.id,
            "order_line": [
                Command.create({
                    "product_id": product.id,
                    "name": f"Room Booking : {self.room_type}",
                    "product_uom_qty": 1,
                    "price_unit": self.total_price,
                }),
            ],
        })


        self.sale_order_id = sale_order.id

        return {
            "type": "ir.actions.act_window",
            "name": _("Customer Sale Order"),
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": sale_order.id,
            "target": "current",
        }


############# INVOICE ###############

# from odoo import models, api, fields, _
# from odoo import Command


# class HotelInvoice(models.Model):
#     _inherit = "hotel.reservation"

#     def action_book_room(self):
#         super(HotelInvoice, self).action_book_room()
#         journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        
#         invoice = self.env["account.move"].create(
#             {
#                 "journal_id": journal.id,
#                 "partner_id": self.guest_id.id,
#                 "move_type": "out_invoice",
#                 "hotel_id": self.hotel_id.id,
#                 "guest_id": self.guest_id.id,
#                 "invoice_line_ids": [
#                     Command.create(
#                         {
#                             "name": self.room_type,
#                             "quantity": 1,
#                             "price_unit": self.total_price,
#                         }
#                     ),
#                     Command.create(
#                         {
#                             "name": "GST",
#                             "quantity": 1,
#                             "price_unit": 100.00,
#                         }
#                     ),
#                 ],
#             }
#         )


#         self.invoice_id = invoice.id

#         # return super().action_book_room()
#         return {
#             "type": "ir.actions.act_window",
#             "name": _("Customer Invoice"),
#             "view_mode": "form",
#             "res_model": "account.move",
#             "res_id": invoice.id,
#             "target": "current",
#         }
    

    
