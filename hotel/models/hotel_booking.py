from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Hotel Booking'

    name = fields.Char(
        required=True, readonly=True, copy=False, default=lambda self: _("New")
    )

    #sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("hotel.booking") or _("New")
            print("\n\n----------------------VALS_LIST-------------------", vals_list)
            print("\n\n..........................VALS.................", vals)

        return super().create(vals_list)

    guest_id = fields.Many2one('guest', required=True)
    phone = fields.Char(related='guest_id.phone')
    aadhaar_id = fields.Char(string="Aadhaar ID", related='guest_id.aadhaar_id')
    pan_card = fields.Char(related='guest_id.pan_card')
    guest_gender = fields.Selection(related='guest_id.gender')
    guest_pic = fields.Image(related='guest_id.guest_image')
    upload_adhar = fields.Image(related='guest_id.upload_adhar')

    hotel_id = fields.Many2one('hotel', string='Hotel Name')

    check_in_date = fields.Date(required=True)
    check_out_date = fields.Date(required=True)
    adults = fields.Integer(required=True)
    children = fields.Integer(required=True)
    total_persons = fields.Integer(string="Total Persons", compute="_compute_total_persons", store=True)
    room_id = fields.Many2one('room', string="Room")
    floor = fields.Integer(related='room_id.floor', readonly=True)
    room_type  = fields.Char()

    # wizard_ids = fields.Many2one('room.availability.wizard')
    guest_line_ids = fields.Many2many('guest')
    policy_ids = fields.One2many('hotel.policy','hotel_id', string="Room Policy", related="hotel_id.policy_ids")

    # pricee_rule_id = fields.Many2one('room.price', store=True)
    applied_pricelist_ids = fields.Many2many('room.price',compute='_compute_applied_pricelists',store=True)

    @api.depends('room_line_ids.price_rule_id')
    def _compute_applied_pricelists(self):
        for record in self:
            record.applied_pricelist_ids = record.room_line_ids.mapped('price_rule_id')


   

    # @api.onchange('hotel_id')
    # def _onchange_hotel_id(self):
    #     if self.hotel_id:
    #         self.policy_ids = self.hotel_id.policy_ids



    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        # ('check_in', 'Check In'),
        # ('check_out', 'Check Out'),
        ('cancelled', 'Cancelled')
    ], string="Status", default="draft")

    @api.depends('adults', 'children')
    def _compute_total_persons(self):
        for record in self:
            record.total_persons = record.adults + record.children

    #python constrain
    @api.constrains('adults', 'children', 'guest_line_ids')
    def _check_guest_line_ids(self):
        for record in self:
            add_guests = len(record.guest_line_ids)
            print("\n\n\n\n\n::::::::::::::::::Add Guest::::",add_guests )

            if record.total_persons > 1 and add_guests < (record.total_persons - 1):
                raise ValidationError(
                    f"You must add at least {record.total_persons - 1} guest's detail"
                )
            
    ##
    @api.constrains('room_line_ids', 'check_in_date', 'check_out_date')
    def _check_room_availability(self):
        for record in self:
            for line in record.room_line_ids:
                overlapping_bookings = self.env['hotel.booking'].search([
                    ('id', '!=', record.id),
                    ('room_line_ids.room_id', '=', line.room_id.id),
                    ('check_in_date', '<', record.check_out_date),
                    ('check_out_date', '>', record.check_in_date),
                    ('status', '!=', 'cancelled'), 
                ])
                if overlapping_bookings:
                    raise ValidationError(
                        f"Room {line.room_id.room_number} is already booked between "
                        f"{record.check_in_date} to {record.check_out_date}."
                    )
                
    ##
    days = fields.Integer(string="Total Days", compute="_compute_days", store=True)

    @api.depends("check_in_date", "check_out_date")
    def _compute_days(self):
        for record in self:
            if record.check_in_date and record.check_out_date:
                record.days = max((record.check_out_date - record.check_in_date).days, 1)

    ##
    total_price = fields.Float(string="Total Price", compute="_compute_total_price", store=True)

    @api.depends('days', 'room_line_ids.price')
    def _compute_total_price(self):
        for record in self:
            room_total = sum(record.room_line_ids.mapped('amount')) 
            record.total_price = record.days * room_total



    ### Add room to booking button
    room_line_ids = fields.One2many('booking.room.line', 'booking_id')

    def action_open_rooms_kanban(self):

        room_ids = self.env['room'].search([('id','in', self.hotel_id.room_ids.ids)])
        for record in room_ids:
            record.is_room_added = False

        booked_room_ids = self.env['hotel.booking'].search([
            ('check_in_date', '<', self.check_out_date),
            ('check_out_date', '>', self.check_in_date),
            ('status', '!=', 'cancelled')
        ]).mapped('room_line_ids.room_id.id')

        room_ids = self.room_line_ids.mapped('room_id').ids
        print("\n\n\n\n\n\n\n\n--------room_ids-------", room_ids)
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Booked Rooms',
            'res_model': 'room',
            'view_mode': 'kanban,form',
            'domain': [('hotel_id', '=', self.hotel_id.id),
                        ('id', 'not in', room_ids),
                        ('id', 'not in', booked_room_ids),
                    ],
            'target': 'current',
        }
    
    #confirm button
    def action_confirm_booking(self):
        print("\n\n\n\nThis is the booking action....")
        for record in self:
            record.status = 'confirmed'

    #cancle button   
    def action_cancel_booking(self):
        for record in self:
            record.status = 'cancelled'

    #create invoice
    def action_create_invoice(self):
        if self.invoice_id:
            raise ValidationError("Invoice has already created for this booking.")
        
            
    #State button 
    invoice_id = fields.Many2one("account.move", readonly=True)

    def action_view_sale_order(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Invoice",
            "view_mode": "form",
            "res_model": "sale.order",
            "res_id": self.invoice_id.id,
            "target": "current",
        }


    order_ids = fields.One2many('restraunt.order', 'booking_id', string="Meal Orders")

    total_order_price = fields.Float(compute="_compute_total_order_price" , store=True)

    @api.depends('order_ids.price')
    def _compute_total_order_price(self):
        for record in self:
            record.total_order_price = sum(record.order_ids.mapped('price'))


    final_amount = fields.Float(compute="_compute_final_amount", store=True)

    @api.depends('total_order_price', 'total_price')
    def _compute_final_amount(self):
        for record in self:
            record.final_amount = record.total_order_price + record.total_price


