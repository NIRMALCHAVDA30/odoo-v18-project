from odoo import api, models, fields
from odoo.exceptions import ValidationError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    max_price = fields.Float(related='product_template_id.max_price')
    min_price = fields.Float(related='product_template_id.min_price')

    @api.constrains('price_unit')
    def _check_min_price(self):

        # max_min_group = self.env.ref('practice.max_min')
        max_min_group = self.env['res.groups'].search([('name', '=', 'Max Min')], limit=1)


        for record in self:
            if max_min_group in self.env.user.groups_id:
                if record.price_unit < record.min_price:
                    raise ValidationError(f"Unit Price cannot be less than the Minimum Price.")
                if record.price_unit > record.max_price:
                    raise ValidationError("Unit Price cannot be more than the Maximum Price.")
            

            