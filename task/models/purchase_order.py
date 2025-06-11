from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


    # Task 10
    name = fields.Char(required=True, copy=False, readonly=True, default='New')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("purchase.order") or _("New")

        return super().create(vals_list)


    # Task 11 
    @api.constrains('order_line')
    def _check_storable_product_confirmation(self):
        for record in self:
            if record.state == 'purchase':
                for line in record.order_line:
                    if line.product_id.type == 'service':
                        raise ValidationError("You cannot have service type products in a confirmed Purchase Order.")

