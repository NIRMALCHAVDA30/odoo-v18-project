from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    # Task 4
    service_total = fields.Float(string="Service Total", compute="_compute_service_total", store=True)
    service_percentage = fields.Float(string="Service %", compute="_compute_service_percentage", store=True)
    other_total = fields.Float(string="Other Total", compute="_compute_other_total", store=True)
    other_percentage = fields.Float(string="Other %", compute="_compute_other_percentage", store=True)



    @api.depends('order_line.price_subtotal', 'order_line.product_id.type')
    def _compute_service_total(self):
        for record in self:
            total = sum(
                line.price_subtotal
                for line in record.order_line
                if line.product_id.type == 'service'
            )
            record.service_total = total

    @api.depends('service_total', 'order_line.price_subtotal')
    def _compute_service_percentage(self):
        for record in self:
            total = sum(line.price_subtotal for line in record.order_line)
            print("\n\n\n----------", total)
            if total:
                record.service_percentage = (record.service_total / total * 100)
            else:
                record.service_percentage = 0.0

    @api.depends('order_line.price_subtotal', 'order_line.product_id.type')
    def _compute_other_total(self):
        for rec in self:
            total = sum(
                line.price_subtotal
                for line in rec.order_line
                if line.product_id.type != 'service'
            )
            rec.other_total = total

    @api.depends('other_total', 'order_line.price_subtotal')
    def _compute_other_percentage(self):
        for rec in self:
            total = sum(line.price_subtotal for line in rec.order_line)
            if total:
                rec.other_percentage = (rec.other_total / total * 100)
            else:
                rec.other_percentage = 0.0
            


    #Task 7 Confirmed SO for the selected customer 
    confirmed_sale_order_count = fields.Integer(compute='_compute_confirmed_sale_order_count')

    def _compute_confirmed_sale_order_count(self):
        for record in self:
            record.confirmed_sale_order_count = self.env['sale.order'].search_count([
                ('partner_id', '=', record.partner_id.id),
                ('state', 'in', ['sale'])
            ])

    def action_view_customer_sale_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Customer Sales Orders',
            'res_model': 'sale.order',
            'view_mode': 'list,form',
            'domain': [
                ('partner_id', '=', self.partner_id.id),
                ('state', 'in', ['sale'])
            ],
        }
    
    #Task 9
    country_of_origin = fields.Many2one('res.country',string="Country of Origin",
                                        compute="_compute_country_of_origin",
                                        store=True)

    @api.depends('partner_id')
    def _compute_country_of_origin(self):
        for record in self:
            print("\n\n\n\n\n\n\n------------------->", self.company_id.country_id)
            print("\n\n\n\n\n<<<<<<<<<<<<<<-------", self.partner_id.country_id)
            record.country_of_origin = record.partner_id.country_id

            print("\n\n", self.partner_id.country_id.name)
            print("\n\n", self.company_id.country_id.name)

    is_invisible = fields.Boolean(compute="_compute_country", store=True)

    @api.depends('partner_id')
    def _compute_country(self):
        for record in self:
            record.is_invisible = record.partner_id.country_id != record.company_id.partner_id.country_id
            print("\n\n\n\n\n\n\n\n\n\n\n==============>",record.is_invisible )




