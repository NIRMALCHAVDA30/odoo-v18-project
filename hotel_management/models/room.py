from odoo import api, models, fields
from odoo.exceptions import ValidationError

class Room(models.Model):
    _name = "room"
    _description = "Hotel Room"
    _rec_name = "room_number"

    room_number = fields.Integer(required=True)
    room_type = fields.Selection(
        [
            ("single", "Single"),
            ("double", "Double"),
            ("suite", "Suite"),
        ],
        required=True,
    )

    price_per_night = fields.Float(required=True)
    hotel_id = fields.Many2one("hotel.management", required=True)
    
    booking_ids = fields.One2many("booking", "room_id", string="Bookings")
    is_available = fields.Boolean(compute="_compute_is_available", store=True, default=True)

    _sql_constraints = [
        ("unique_room_number", "unique(room_number)", "Room Number must be unique!"),
    ]

    @api.depends("booking_ids.status")
    def _compute_is_available(self):
        for record in self:
            active_bookings = record.booking_ids.filtered(lambda a: a.status in ["booked", "check_in"])
            record.is_available = not bool(active_bookings)



    max_persons = fields.Integer(string="Maximum Persons Allowed", required=True, default=2)
    extra_person_charge = fields.Float(string="Extra Person Charge", required=True)

    room_image = fields.Image()

