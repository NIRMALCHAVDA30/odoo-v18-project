from odoo import api, models, fields

class Guest(models.Model):
    _name = "guest"
    _description = "Hotel Guest"

    name = fields.Char()
    phone = fields.Char()
    # guest_id  = fields.Integer()
    