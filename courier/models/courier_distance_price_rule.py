from odoo import models, fields, api

class CourierDistancePriceRule(models.Model):
    _name = 'courier.distance.price.rule'
    _description = 'Courier Distance Price Rule'

    name = fields.Char()
    minimum_distance = fields.Float()
    maximum_distance = fields.Float()
    price = fields.Float()