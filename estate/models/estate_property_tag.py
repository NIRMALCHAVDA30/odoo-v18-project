from odoo import api, models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "This is Estate Property Tag Module"
    _rec_name = "name"
    _order = "name"

    name = fields.Char("Name" ,required=True)

    _sql_constraints = [
        ("unique_property_tag", "UNIQUE(name)", "Tag name must be unique"),
    ]

    color = fields.Integer()  