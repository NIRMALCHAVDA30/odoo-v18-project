from odoo import models, fields, api
from datetime import date, timedelta

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _order = 'amount_total desc'


    # Identify the top 5 customers by purchase amount in the last 6 months.
    def top_5_customers_last_6_months(self):
        today = date.today()
        six_months_ago = today - timedelta(days=180)

        sale_orders = self.env['purchase.order'].search([
            ('date_approve', '>=', six_months_ago),
            ('date_approve', '<=', today),
            ('state', 'in', ['purchase'])
        ], limit=5)

        print("\n\n\n---sale_orders---->", sale_orders.mapped('partner_id.name'))

        return {
                'type': 'ir.actions.act_window',
                'name': 'Top 5 Customer',
                'res_model': 'purchase.order',
                'view_mode': 'list,form',
                'domain': [('id', 'in', sale_orders.ids)],
            }