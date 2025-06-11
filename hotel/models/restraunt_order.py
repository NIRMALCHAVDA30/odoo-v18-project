from odoo import models, fields, api

class RestrauntOrder(models.Model):
    _name = 'restraunt.order'
    _description = 'Restraunt order'
    _rec_name = 'booking_id'

    booking_id = fields.Many2one('hotel.booking')
    food_id = fields.Many2one('restraunt.food', string="Food Item", required=True)
    price = fields.Float(related='food_id.price', string="Price", store=True)
