from odoo import models

class ProductTemplate(models.Model):
    _inherit = 'product.template'


    #Task 2:Find all products that have never been sold.
    def action_show_never_sold_products(self):
        never_sold_products = self.env['product.product'].search([
            ('id', 'not in', self.env['sale.order.line'].search([
                ('product_id', '!=', False)
            ]).mapped('product_id').ids)
        ])

        return {
            'type': 'ir.actions.act_window',
            'name': 'Products Never Sold',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', never_sold_products.ids)],
        }
    
    #Task : Find products sold with a discount > 30%.
    def products_sold_with_a_discount(self):
        sold_product_discount = self.env['product.product'].search([
            ('id', 'in', self.env['sale.order.line'].search([
                ('state', 'in', ['sale']),
                ('discount', '>', 30 ),
            ]).mapped('product_id').ids)
        ])

        print("\n\n\n\n-----------sold_product_discount--------->",sold_product_discount.ids)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sold Discount',
            'res_model': 'product.product',
            'view_mode': 'list,form',
            'domain': [('id', 'in', sold_product_discount.ids)],
        }
