from odoo import models, fields

class RoomType(models.Model):
    _name = 'room.type'
    _description = 'Hotel Room Type'

    
    name = fields.Char()
    capacity = fields.Integer()
    price = fields.Float()
    ac = fields.Selection([
        ('ac' , 'AC'),
        ('non ac', 'Non AC')
    ],default='ac')







