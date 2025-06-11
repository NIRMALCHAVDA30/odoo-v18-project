from odoo import models, fields, api

class CourierDimensionPriceRule(models.Model):
    _name = 'courier.dimension.price.rule'
    _description = 'Courier Dimension Price Rule'

    name = fields.Char()
    length = fields.Integer()
    width = fields.Integer()
    height = fields.Integer()
    volumetrice_Weight = fields.Float(string="Volumetrice Weight(kg)")
    price = fields.Float()