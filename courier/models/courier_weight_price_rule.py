from odoo import models, fields, api

class CourierWeightPriceRule(models.Model):
    _name = 'courier.weight.price.rule'
    _description = 'Courier Weight Price Rule'

    name = fields.Char()
    minimum_weight = fields.Float()
    maximum_weight = fields.Float()
    price = fields.Float()