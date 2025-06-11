from odoo import models, fields, api

class CourierType(models.Model):
    _name = 'courier.type'
    _description = 'Courier Type'

    name = fields.Char(string="Type Name")