from odoo import models, fields, api

class CourierCategories(models.Model):
    _name = 'courier.categories'
    _description = 'Courier Categories'

    name = fields.Char(string="Categories Name")