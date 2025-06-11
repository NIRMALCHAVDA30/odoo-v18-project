from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    # Task 8
    # terms_conditions = fields.Html(string="Terms and Conditions")

    def _get_new_picking_values(self):
        vals = super()._get_new_picking_values()

        vals['terms_conditions'] = self.group_id.sale_id.note
        # print("\n\n\n---------->", self.group_id)
        return vals
    