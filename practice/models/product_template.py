from odoo import api, models, fields

class ProductTemplate(models.Model):
    _inherit = "product.template"

    min_price = fields.Float()
    max_price = fields.Float()