from odoo import models, fields,api

class HotelRoom(models.Model):
    _name = 'room'
    _description = 'Hotel Room'
    _rec_name = "room_number"

    hotel_id = fields.Many2one('hotel', string='Hotel')
    room_number = fields.Char(string='Room Number', required=True)
    floor = fields.Integer(required=True)
    status = fields.Selection([
        ('available', 'Available'),
        ('maintenance', 'Maintenance')], string='Status', default='available')
    
    room_image = fields.Image()

    _sql_constraints = [
        ("unique_room_number", "unique(room_number)", "Room Number must be unique!"),
    ]

    room_type_id = fields.Many2one("room.type" , required=True)
    price_per_night = fields.Float(required=True)

    @api.onchange('room_type_id') 
    def _onchange_room_type_id(self):
        if self.room_type_id:
            self.price_per_night = self.room_type_id.price 
        else:
            self.price_per_night = 0.0  

    policy_ids = fields.Many2many('hotel.policy', string="Room Policy")

    capacity = fields.Integer(related='room_type_id.capacity', required=True)
    room_specification_ids = fields.Many2many('room.specifications')

    # is_booked = fields.Boolean(default=False)
    is_room_added  = fields.Boolean(default=False)
    
    ##
    def action_open_booking(self):

        room_ids = self.search([('id','in', self.hotel_id.room_ids.ids)])
        print("\n\n\n\n------------ROOM ID ----", room_ids)
        for room in room_ids:
                room.is_room_added = True
    

        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Booking',
            'res_model': 'hotel.booking',
            'view_mode': 'form',
            'target': 'current',
            'context': {
                'default_room_id': self.id,
                'default_hotel_id': self.hotel_id.id, 
               
                'default_check_in_date': self._context.get('check_in_date'),
                'default_check_out_date': self._context.get('check_out_date'),
                'default_adults': self._context.get('adults'),
                'default_children': self._context.get('children'), 

                ##
                'default_room_line_ids': [(0, 0, {
                'room_id': self.id,
                'price': self.price_per_night, 
                'floor': self.floor,
                'room_type': self.room_type_id.name,
                })],
            },
        }
    
    ###
    def action_add_to_booking(self):
        active_id = self.env.context.get('active_id')  # ID of the active booking
        print("\n\n\n\n>>>>>>>>>>>>>>active_id>>>>>>>",active_id )
        
        # for booking in self:
        #     for room in booking.hotel_id.room_ids:
        #         room.is_room_added = False
   
        if active_id:
            booking_id = self.env.context.get('active_id')
            booking = self.env['hotel.booking'].browse(booking_id) #fetch

            self.env['booking.room.line'].create({
                'booking_id': booking.id,
                'room_id': self.id,
                'room_type': self.room_type_id.name,
                'floor': self.floor,
            })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.booking',
            'res_id': booking.id,
            'view_mode': 'form',
            'target': 'current',
        }





