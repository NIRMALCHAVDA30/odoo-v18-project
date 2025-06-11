from odoo import models, fields, api

class ProductProduct(models.Model):
    _inherit = 'product.product'

    #task 2
    @api.model
    def product_product(self):
        if self.order_line.product_id:
            product = self.env['sale.order'].search([
                ('state', '!=', 'sale')
            ])
            print("\n\n\n-------->", product)