from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def open_wizard(self):
        return{
            'type' : 'ir.actions.act_window',
            'name': 'Set Unit Price',
            'res_model': 'price.wizard',
            'view_mode' : 'form', 
            'target' : 'new',
            'context' : {'default_order_id': self.id},
        }