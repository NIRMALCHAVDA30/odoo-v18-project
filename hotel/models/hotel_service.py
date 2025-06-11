from odoo import models, fields

class HotelService(models.Model):
    _name = 'hotel.service'
    _description = 'Hotel Services'

    name = fields.Char(string='Service Name', required=True)
    description = fields.Text()
    lunch_service = fields.Boolean(string='Lunch Service Available')
