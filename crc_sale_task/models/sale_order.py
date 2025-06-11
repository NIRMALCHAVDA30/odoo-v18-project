from odoo import models, fields, api
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from  datetime import date
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    crc_subscription = fields.Boolean(string='Subscription')
    crc_subscription_plan_id = fields.Many2one('subscription.plan', string='Subscription Plan')
    crc_next_so_date = fields.Date(string='Next SO Date')


    # Age Birth task
    birth_date = fields.Date()
    age = fields.Integer(compute="_compute_birth", store=True)


    @api.depends('birth_date')
    def _compute_birth(self):
        today = date.today()
        # self.birth_date = False
        for record in self:
            if record.birth_date:
                if record.birth_date > today:
                    raise ValidationError("You cannot enter a future birth date.")
                if record.birth_date:
                    record.age = today.year - record.birth_date.year - (
                        (today.month, today.day) < (record.birth_date.month, record.birth_date.day)
                    )
            else:
                record.birth_date = False
    ###

    @api.model
    def create_record(self):
        print("\n\n\n------------------->")
        pass

        # today = fields.Date.today()
        # orders = self.search([
        #     ('crc_subscription', '=', True),
        #     ('state', 'in', ['sale', 'done']),
        #     ('sale_order_template_id', '!=', False),
        #     ('crc_subscription_plan_id', '!=', False)
        # ])

        # for order in orders:
        #     plan = order.crc_subscription_plan_id
        #     start_date = order.date_to_validate
        #     if not plan or not start_date:
        #         continue

        #     # Compute next date from "date to be validated"
        #     delta = relativedelta(**{plan.period: plan.interval})
        #     next_date = start_date + delta

        #     if next_date == today:
        #         # Create a new SO in draft using the same template
        #         new_so_vals = {
        #             'partner_id': order.partner_id.id,
        #             'crc_subscription': order.crc_subscription,
        #             'crc_subscription_plan_id': order.crc_subscription_plan_id.id,
        #             'sale_order_template_id': order.sale_order_template_id.id,
        #             'origin': order.name,
        #             'date_to_validate': today,  # reset for next cycle
        #         }

        #         # Use template to populate order lines
        #         template = order.sale_order_template_id
        #         if template:
        #             lines = []
        #             for t_line in template.sale_order_template_line_ids:
        #                 if t_line.product_id:
        #                     lines.append((0, 0, {
        #                         'product_id': t_line.product_id.id,
        #                         'product_uom_qty': t_line.product_uom_qty,
        #                         'price_unit': t_line.product_id.lst_price,
        #                         'name': t_line.name or t_line.product_id.name,
        #                     }))
        #             new_so_vals['order_line'] = lines

        #         self.env['sale.order'].create(new_so_vals)



#########
    