from odoo import models, fields, api
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'


    x_requires_approval = fields.Boolean(string="Requires Approval")
   

    def action_confirm(self):
        for record in self:
            if record.x_requires_approval:
                if self.env.user.has_group('sales_team.group_sale_manager') or self.env.user.has_group('sales_team.group_sale_salesman_all_leads'):
                    record.x_requires_approval = True
                else:
                    raise UserError("Approval by a Administrator before confirmation.")
            
            return super(SaleOrder, self).action_confirm()
        





