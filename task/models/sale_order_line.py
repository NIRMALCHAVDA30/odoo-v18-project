from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_available_qty = fields.Float(string="Available Qty",related='product_id.qty_available')
