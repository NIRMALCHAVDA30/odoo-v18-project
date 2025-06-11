from odoo import models, fields, api

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    # sale_order_id = fields.Many2one('sale.order')
    partner_id = fields.Many2one('res.partner')

    