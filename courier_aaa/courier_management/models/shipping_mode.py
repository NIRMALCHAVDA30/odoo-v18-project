from odoo import models, api, fields 
from odoo.exceptions import UserError 
from datetime import date, timedelta


class ShippingMode(models.Model):
    _name = 'shipping.mode'
    
    name = fields.Char()
    speed_rank = fields.Selection(
        selection = [('cheapest','Cheapest'),('balanced','Balanced'),('fastest','Fastest')],
        string = "Speed Rank"
    )