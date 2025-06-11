from odoo import models, fields, api
from datetime import date

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    # Task 1 : Get all confirmed sale orders that contain at least one product from a specific category.
    def action_show_category_orders(self):
        category_id = 1  #
        confirmed_orders = self.search([
            ('state', '=', 'sale'),
            ('order_line.product_id.categ_id', '=', category_id)
        ])
        print("\n\n\n---------->", confirmed_orders.ids)
        # return confirmed_orders
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Confirmed Orders by Category',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', confirmed_orders.ids)],
        }
    

    

    # Task 9:ake a new partner_id field on  Quotation Template (sale.order.template) if customer is selected on SO , only the Quotation template of selected customer should be shown
    sale_order_template_id = fields.Many2one('sale.order.template', compute='_compute_sale_order_template_id',store=True)

    @api.depends('partner_id')
    def _compute_sale_order_template_id(self):
        for record in self:
            if record.partner_id:
                template = self.env['sale.order.template'].search([
                    ('partner_id', '=', record.partner_id.id)
                ], limit=1)
                record.sale_order_template_id = template
            else:
                record.sale_order_template_id = False 


    # Task : Return all salespeople with no sales this month.
    def salespeople_with_no_sales_this_month(self):
        today = date.today()
        print("\n\n\n-----today--->", today)
        start_date = today.replace(day=1) 
        print("\n\n\n----start_date->", start_date)
        end_date = today.replace(day=28)
        print("\n\n\n-----end_date-->", end_date)

        salespeople_with_sales = self.env['sale.order'].search([
            ('user_id', '!=', False),  
            ('state', 'in', ['sale']),
            ('date_order', '>=', start_date),
            ('date_order', '<=', end_date)
        ]).mapped('user_id')

        all_users = self.env['res.users'].search([])

    
        salespeople_with_no_sales = all_users.filtered(lambda x: x not in salespeople_with_sales)

        print("\n\n\n\n", salespeople_with_no_sales.mapped('name'))

        return {
            'type': 'ir.actions.act_window',
            'name': 'Users with No Sales',
            'res_model': 'res.users',
            'view_mode': 'list,form',
            'domain': [('id', 'in', salespeople_with_no_sales.ids)],
        }
    

    # Find partners with a Canceled Sale Order.
    def cancel_sale_order(self):
        cancel = self.search([
            ('state', 'in', ['cancel'])
        ])

        sale_order = cancel.mapped('partner_id')
        print("\n\n\n---------Cancel Sale Order---->", sale_order.mapped('name'))


    # Return sales orders with a discount greater than 20%.
    # in the discount field activate in the sales settings.
    def discount_greater_than_20(self):
        sale_discount = self.env['sale.order.line'].search([
            ('discount', '>', 20 ),
            ('state', 'in', ['sale'])
        ])

        print("\n\n\n------Sale order discount----->", sale_discount)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale order discount',
            'res_model': 'sale.order.line',
            'view_mode': 'list,form',
            'domain': [('id', 'in', sale_discount.ids)],
        }
    
 
