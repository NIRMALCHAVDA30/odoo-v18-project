from odoo import api, models, fields

class HotelGuest(models.Model):
    _name = "hotel.guest"
    _description = "Hotel Guest"

    # name = fields.Many2one("res.partner" ,required=True, string="Guest Name")
    # email = fields.Char(string="Email Address" ,related="name.email")
    # phone = fields.Char(required=True, string="Contact Number" ,size=10, related="name.phone")
    # id_proof = fields.Char(required=True, string="Identity proof")
    # nationality = fields.Char()
    # preferences = fields.Text(string="Guest preferences")

    
    # name = fields.Many2one("res.partner", required=True, string="Guest Name")
    bookingg_ids = fields.One2many("hotel.reservation", "guest_id", string="Guest History")

    # guest_with_bookings = fields.Many2many("res.partner")

    # @api.depends("bookingg_ids")
    # def _compute_guest_with_bookings(self):
    #     booked_guest_ids = self.env["hotel.reservation"].search([]).mapped("guest_id.id")
    #     self.guest_with_bookings = booked_guest_ids   # Assign the IDs directly

    # @api.onchange("name")
    # def _onchange_name(self):
    #     if self.name:
    #         self.bookingg_ids = self.env["hotel.reservation"].search([("guest_id", "=", self.name.id)])   
    #     else:
    #         self.bookingg_ids = False
