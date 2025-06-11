from odoo import models, fields, api

class CourierPriorities(models.Model):
    _name = 'courier.priorities'
    _description = 'Courier Priorities'

    name = fields.Char(string="Priorities Name")
    charges = fields.Float()