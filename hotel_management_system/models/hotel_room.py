from odoo import api, models, fields
from odoo.exceptions import ValidationError


class HotelRoom(models.Model):
    _name = "hotel.room"
    _description = "Hotel Room"
    _rec_name = "name"

    name = fields.Char(required=True, string="Room Number")
    room_type = fields.Selection(
        [
            ("single", "Single"),
            ("double", "Double"),
            ("suite", "Suite"),
        ],
        required=True,
    )

    price_per_night = fields.Float(required=True, string="Room price per night")
    state = fields.Selection(
        [
            ("available", "Available"),
            ("occupied", "occupied"),
            ("maintenance", "Maintenance"),
        ]
    )

    floor = fields.Integer(string="Floor number")

    hotel_id = fields.Many2one("hotel.management", required=True)

    booking_ids = fields.One2many("hotel.reservation", "room_id", string="Bookings(history)")
    is_available = fields.Boolean(
        compute="_compute_is_available", store=True, default=True
    )

    _sql_constraints = [
        ("unique_room_number", "unique(name)", "Room Number must be unique!"),
    ]

    @api.depends("booking_ids.status")
    def _compute_is_available(self):
        for record in self:
            active_bookings = record.booking_ids.filtered(
                lambda a: a.status in ["booked", "check_in"]
            )
            record.is_available = not bool(active_bookings)

    max_persons = fields.Integer(
        string="Maximum Persons Allowed", required=True, default=2
    )
    extra_person_charge = fields.Float(string="Extra Person Charge", required=True)

    room_image = fields.Image() 

    housekeeping_status = fields.Selection([
        ("pending" , "Pending"),
        ("in_maintenance", "In Maintenance"),
        ("cleaned", "Cleaned"),
    ] ,default="pending")

    @api.onchange('housekeeping_status')
    def _onchange_housekeeping_status(self):
        for room in self:
            if room.housekeeping_status == "cleaned":
                room.state ="available"
            elif room.housekeeping_status == "pending":
                room.state = "occupied"
            elif room.housekeeping_status == "in_maintenance":
                room.state = "maintenance"

    

    ###############
    # product_id = fields.Many2one("hotel.reservation")



    

