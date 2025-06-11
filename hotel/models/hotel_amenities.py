from odoo import models, fields

class HotelAmenities(models.Model):
    _name = 'hotel.amenities'
    _description = 'Hotel Amenities'

    name = fields.Char(string='Amenity Name', required=True)
    amenities_type = fields.Selection([
        ('garden', 'Garden'),
        ('swimmingpool', 'Swimmingpool'),])
    description = fields.Text(string='Description')
