from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Task 4
    @api.model
    def inventory_admin(self):
        for record in self:
            if self.env.user.has_group('stock.group_stock_manager'):
                accsess = self.env.user.has_group('stock.group_stock_manager').browse(record.partner_id)

                print("\n\n\n******************>",accsess)
