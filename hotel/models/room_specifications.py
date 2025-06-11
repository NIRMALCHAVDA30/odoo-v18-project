from odoo import models, fields

class RoomSpecifications(models.Model):
    _name = 'room.specifications'
    _description = 'Hotel Room Specifications'

    name = fields.Char(string='Specification Name', required=True)
    description = fields.Text()
