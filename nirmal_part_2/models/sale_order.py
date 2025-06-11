from odoo import models, fields, api
from datetime import date, timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    #Task 9
    partner_id = fields.Many2one('res.partner', compute="_compute_template", store=True)
    sale_order_template_id = fields.Many2one('sale.order.template')

    @api.depends('partner_id','sale_order_template_id')
    def _compute_template(self):
        for record in self:
            if record.partner_id:
                record.sale_order_template_id = record.sale_order_template_id.name

            else:
                record.partner_id = False


    #task 3
    month = date.today() - timedelta(days=30)

    def salespeople_this_month(self):
        this_month = self.env['sale.order'].search([
            ('state', '=', 'sale'),
            ('date_order', '<=', self.month)
        ])

        salespeople = this_month.mapped('user_id')
        print("\n\n\n--------->", salespeople.name)