from odoo import models, fields

class ShippingMode(models.Model):
    _name = 'shipping.mode'
    _description = 'Shipping Mode'

    name = fields.Char(string="Mode Name", required=True)
    speed_rank = fields.Selection([
        ('cheapest', 'Cheapest'),
        ('fastest' , 'Fastest'),
        ('balanced', 'Balanced')
    ])
