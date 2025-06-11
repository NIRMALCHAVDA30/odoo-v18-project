from odoo import models, fields

class HotelPolicy(models.Model):
    _name = 'hotel.policy'
    _description = 'Hotel Policy'

    name = fields.Char(string='Hotel Policy Name', required=True)
    description = fields.Text()

    hotel_id = fields.Many2one('hotel', string="Hotel")
