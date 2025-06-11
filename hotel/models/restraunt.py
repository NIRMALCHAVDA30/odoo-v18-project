from odoo import models, fields, api

class Restaurant(models.Model):
    _name = 'restaurant'
    _description = 'Additional Restaurant Services'

    name = fields.Char()
    hotel_id = fields.Many2one('hotel')

    food_ids = fields.One2many('restraunt.food', 'restaurant_id', string="Food Items")
