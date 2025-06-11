from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomAvailabilityWizard(models.TransientModel):
    _name = 'room.availability.wizard'
    _description = 'Hotel Room Availability Wizard'

    check_in_date = fields.Date(string="Check-in Date", required=True, default=fields.Date.today)
    check_out_date = fields.Date(string="Check-out Date", required=True)
    adults = fields.Integer(required=True, default=1)
    children = fields.Integer(default=0)
    hotel_id = fields.Many2one('hotel', string="Hotel", readonly=True)
    


    @api.constrains('check_in_date', 'check_out_date')
    def _check_dates(self):
        for record in self:
            today = fields.Date.today()
            if record.check_in_date < today:
                raise ValidationError("Check-in date cannot be in the past.")
            if record.check_in_date > record.check_out_date:
                raise ValidationError("Check-out date must be after check-in date.")
            
            
    @api.constrains('adults', 'children')
    def _check_guest_count(self):
        for record in self:
            if record.adults + record.children < 1:
                raise ValidationError("At least one guest (adult or child).")

    
    #wizard buttons
    def action_show_rooms(self):
        
        for rec in self.hotel_id.room_ids:
            rec.is_room_added = True


        booked_rooms = self.env['booking.room.line'].search([
            ('check_in', '<=', self.check_out_date),
            ('check_out', '>=', self.check_in_date),
            ('room_id.hotel_id', '=', self.hotel_id.id)
        ])

        booked_room_ids = booked_rooms.mapped('room_id.id')
    

        domain = [
            ('hotel_id', '=', self.hotel_id.id),
            ('capacity', '>=', self.adults + self.children),
            ('status', '=', 'available'),
            ('id', 'not in', booked_room_ids),
        ]

        # rooms = self.env['room'].search(domain)

        # if not rooms:
        #     return {
        #         'type': 'ir.actions.client',
        #         'tag': 'display_notification',
        #         'params': {
        #             'title': 'No Rooms Available',
        #             'message': 'Sorry, no rooms are available for the selected person.',
        #             'type': 'warning',
        #         }
        #     }
        
        print("\n\n\n\n\n\n>>>>>>self.env.ref('hotel.room_hotel_wizard_view_kanban').id",self.env.ref('hotel.room_hotel_wizard_view_kanban').id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Available Rooms',
            'res_model': 'room',
            'view_mode': 'kanban,form',
            'views': [(self.env.ref('hotel.room_hotel_wizard_view_kanban').id, 'kanban'), (self.env.ref('hotel.room_hotel_wizard_view_form').id, 'form')],
            # 'view_id': self.env.ref('hotel.room_hotel_wizard_view_kanban').id,
            'domain': domain,
            'target': 'current',
            'context': {
                'check_in_date': self.check_in_date,
                'check_out_date': self.check_out_date,
                'adults': self.adults,
                'children': self.children,
            },
        }

    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close'}
    




