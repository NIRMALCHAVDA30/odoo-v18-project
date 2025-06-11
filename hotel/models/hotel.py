from odoo import models, fields

class Hotel(models.Model):
    _name = 'hotel'
    _description = 'Hotel Details'

    name = fields.Char(string='Hotel Name', required=True)
    location = fields.Char()
    landmark = fields.Char()
    # policies = fields.Text()
    rating = fields.Selection([
        ('below average ' ,'Below Average '),
        ('satisfactory', 'Satisfactory'),
        ('good' , 'Good'),
        ('excellent', 'Excellent'),
    ])

    room_ids = fields.One2many('room', 'hotel_id', string="Rooms")
    amenities_ids = fields.Many2many('hotel.amenities')
    service_ids = fields.Many2many('hotel.service', string="Services")

    policy_ids = fields.One2many('hotel.policy', 'hotel_id', string="Hotel Policies")

    hotel_image = fields.Image()

    #button wizard
    def action_show_available_rooms(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Check Availability',
            'res_model': 'room.availability.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_hotel_id': self.id}
        }
