from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def bought_product(self):
        for record in self:
            product = self.env['product.product'].browse(record.product_id)

            sales = self.env['sale.order.line'].search_count([
                ('product_id', '=', product.id), 
            ])
            print("\n\n\n------------->", sales)


    
