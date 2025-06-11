from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class HotelReservation(models.Model):
    _name = "hotel.reservation"
    _description = "Hotel Booking"

    name = fields.Char(
        required=True, readonly=True, copy=False, default=lambda self: _("New")
    )

    #sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("hotel.reservation") or _("New")
            print("\n\n----------------------VALS_LIST-------------------", vals_list)
            print("\n\n..........................VALS.................", vals)

        return super().create(vals_list)

    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date(required=True)
    total_price = fields.Float(compute="_compute_total_price", store=True)

    # guest_id = fields.Many2one("hotel.guest", string="Guest", required=True)
    guest_id = fields.Many2one("res.partner",domain=[('is_guest', '=', True)], string="Guest")
    hotel_id = fields.Many2one("hotel.management", required=True)

    aadhar_card = fields.Char(size=12)  
    pan_card = fields.Char(size=8)

    room_type = fields.Selection(
        [
            ("single", "Single"),
            ("double", "Double"),
            ("suite", "Suite"),
        ],
        required=True,
    )

    status = fields.Selection(
        [
            ("booked", "Booked"),
            ("check_in", "Check-in"),
            ("check_out", "Check-out"),
            ("cancelled", "Cancelled"),
        ],
        # default="booked",
        string="Booking Status",
    )

    room_id = fields.Many2one(
        "hotel.room",
        # domain="[('room_type', '=', room_type), ('hotel_id', '=', hotel_id)]",
        required=True,
    )

    # Available room
    available_room_ids = fields.Many2many("hotel.room", compute="_compute_available_rooms", store=True)

    @api.depends("check_in_date", "check_out_date")
    def _compute_available_rooms(self):
            print('\n\n!!!!!!!!!!!!!!!!!!!!!!compute available')
            if self.check_in_date and self.check_out_date:
                available_rooms = self._get_available_rooms(self.check_in_date, self.check_out_date)
                self.available_room_ids = available_rooms.ids

    def _get_available_rooms(self, check_in_date, check_out_date):
        print("\n\n-------------------- METHODDDDDD")
        overlap_bookings = self.env["hotel.reservation"].search([
            ("check_in_date", "<=", check_out_date),
            ("check_out_date", ">=", check_in_date)
        ])
        booked_rooms = overlap_bookings.mapped("room_id")
        print("\n\n-----------------------BOOKED ROOM", booked_rooms)

        available_rooms = self.env["hotel.room"].search([
            ("id", "not in", booked_rooms.ids)
            # ("is_available", "=", True)
        ])
        print("\n\n------------------------AVAILABLE ROOMS", available_rooms)
        return available_rooms

    # @api.depends("room_id", "check_in_date", "check_out_date")
    # def _compute_total_price(self):
    #     for record in self:
    #         if record.room_id and record.check_in_date and record.check_out_date:
    #             days = (record.check_out_date - record.check_in_date).days or 1
    #             record.total_price = record.room_id.price_per_night * days

    # python inheritance
    @api.constrains("check_in_date", "check_out_date", "room_id")
    def _check_room_availability(self):
        for record in self:
            print(
                "\n\n\n\n>>>>>>>>>>>>>DATE..",
                record.check_out_date < record.check_in_date,
            )
            print(
                "\n\n\n\n>>...........DATE..",
                record.check_out_date <= record.check_in_date,
            )
            if record.check_out_date < record.check_in_date:
                raise ValidationError(
                    "Check-out date (big)greater than check-in date!!"
                )

            # Check bookings for the same room
            date_bookings = self.env["hotel.reservation"].search(
                [
                    ("room_id", "=", record.room_id.id),
                    ("status", "in", ["booked", "check_in"]),
                    ("id", "!=", record.id),
                    "|",
                    "&",
                    ("check_in_date", "<", record.check_out_date),
                    ("check_out_date", ">", record.check_in_date),
                    "&",
                    ("check_in_date", "<=", record.check_in_date),
                    ("check_out_date", ">", record.check_in_date),
                ]
            )

            if date_bookings:
                raise ValidationError(
                    f"Room {record.room_id.room_number} is already booked during the selected dates!"
                )

    def action_cancel_booking(self):
        for record in self:
            if record.status == "cancelled":
                raise ValidationError("Booking is already cancelled!")
            record.status = "cancelled"

    def action_book_room(self):
        print("\n\n\n\n\n\n\n\n\n.......button was clicked")
        for record in self:
            record._check_room_availability()
            record.status = "booked"
            # record.write({'status': 'booked'}) 

    # def action_check_out(self):
    #     for record in self:
    #         if record.status != 'check_in':
    #             raise ValidationError("Cannot check out unless the guest has checked in!")
    #         record.status = 'check_out'

    #
    num_guests = fields.Integer(string="Number of Guests", default=1, required=True)

    max_persons = fields.Integer(string="Max Persons", compute="_compute_max_persons", store=True)
    extra_person_charge = fields.Float(string="Extra Person Charge", compute="_compute_extra_person_charge", store=True)

    extra_person_cost = fields.Float(compute="_compute_extra_person_cost", store=True)

    extra_charge_ids = fields.Many2many("extra.charges", string="Extra Charges(Facility)")
    extra_charges_total = fields.Float(
        compute="_compute_extra_charges_total", store=True
    )

    days = fields.Integer(string="Total Days", compute="_compute_days", store=True)

    @api.depends("check_in_date", "check_out_date")
    def _compute_days(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                record.days = max((record.check_out_date - record.check_in_date).days, 1)
            else:
                record.days = 0

    @api.depends("room_id")  # fetch
    def _compute_max_persons(self):
        for record in self:
            if record.room_id:
                record.max_persons = record.room_id.max_persons
            else:
                record.max_persons = 0

    @api.depends("room_id")  # fetch
    def _compute_extra_person_charge(self):
        for record in self:
            if record.room_id:
                record.extra_person_charge = record.room_id.extra_person_charge
            else:
                record.extra_person_charge = 0

    @api.depends("num_guests", "max_persons", "extra_person_charge")  # extra cost
    def _compute_extra_person_cost(self):
        for record in self:
            if record.num_guests > record.max_persons:
                extra_people = record.num_guests - record.max_persons
                record.extra_person_cost = (extra_people * record.extra_person_charge * record.days)
            else:
                record.extra_person_cost = 0

    @api.depends("extra_charge_ids")  # extra charges on selectednum_guests options
    def _compute_extra_charges_total(self):
        for record in self:
            total = 0
            for charge in record.extra_charge_ids:
                if charge.charge_type == "per_person":
                    total = total + charge.total_cost
                else:
                    total = total + charge.total_cost
            record.extra_charges_total = total

    @api.depends("room_id","check_in_date","check_out_date","extra_person_cost","extra_charges_total")
    def _compute_total_price(self):
        for record in self:
            if record.room_id and record.check_in_date and record.check_out_date:
                days = (record.check_out_date - record.check_in_date).days or 1
                room_cost = record.room_id.price_per_night * days
                record.total_price = (
                    room_cost + record.extra_person_cost + record.extra_charges_total
                )

    # python constrains
    @api.constrains("num_guests", "max_persons")
    def _check_max_person_limit(self):
        for record in self:
            if record.num_guests < 1:
                raise ValidationError("Number of guests cannot be less than 1!")
            if record.num_guests > (record.max_persons + 2):  # Allow 2 extra guest max
                raise ValidationError(
                    f"Maximum allowed guests for this room is {record.max_persons + 2}!")


    ###
    payment_status = fields.Selection([
        ('pending' , 'Pending'),
        ('paid', 'Paid')
    ], default="pending") 

    invoice_id = fields.Many2one("account.move", string="Invoice Id Number", readonly=True)    


    ###State button Sale order
    sale_order_id = fields.Many2one("sale.order", string="Sale Order", readonly=True)

    def action_view_sale_order(self):
        return {
            "type": "ir.actions.act_window",
            "name": _("Sale Order"),
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": self.sale_order_id.id,
            "target": "current",
        }
    

    ### Partial payment
    # amount_paid = fields.Float(compute="_compute_amount_paid", store=True)
    # amount_due = fields.Float(string="Amount Due", compute="_compute_amount_paid", store=True)
    # payment_status = fields.Selection([
    #     ('pending', 'Pending'),
    #     ('partial', 'Partially Paid'),
    #     ('paid', 'Paid')
    # ], string="Payment Status", compute="_compute_amount_paid", store=True)

    # @api.depends('invoice_id.payment_state')
    # def _compute_amount_paid(self):
    #     for record in self:
    #         if record.invoice_id:
    #             record.amount_paid = record.invoice_id.amount_total - record.invoice_id.amount_residual
    #             record.amount_due = record.invoice_id.amount_residual
                
    #             if record.invoice_id.payment_state == 'paid':
    #                 record.payment_status = 'paid'
    #             elif record.invoice_id.payment_state == 'partial':
    #                 record.payment_status = 'partial'
    #             else:
    #                 record.payment_status = 'pending'
    #         else:
    #             record.amount_paid = 0.0
    #             record.amount_due = record.amount_total
    #             record.payment_status = 'pending'


