from odoo import models, fields, api

class SaleOrderTemplate(models.Model):
    _inherit = 'sale.order.template'

    # task 9
    partner_id = fields.Many2one('res.partner')