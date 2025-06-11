from odoo import models, fields, api

class CourierTag(models.Model):
    _name = 'courier.tag'
    _description = 'Courier Tag'

    name = fields.Char(string="Tag Name")
    color = fields.Integer()