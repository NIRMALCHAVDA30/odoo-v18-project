from odoo import models, fields, api

class RoomPrice(models.Model):
    _name = 'room.price'
    _description = 'Hotel Room Pricing'


    name = fields.Char(string='Pricelist Name', required=True)
    # season_id = fields.Many2one('room.season', string='Season')
    item_ids = fields.One2many('room.pricelist', 'price_id', string='Price Rules')
    hotel_id = fields.Many2one('hotel')
