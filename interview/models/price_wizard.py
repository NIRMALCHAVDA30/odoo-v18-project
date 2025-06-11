from odoo import models, fields, api

class PriceWizard(models.TransientModel):
    _name = 'price.wizard'
    _description = 'This the the price wizard'

    prices = fields.Float(string="Price")
    order_id = fields.Many2one('sale.order')

    def action_apply_prices(self):
        print("\n\n\n------>", self.order_id)
        for record in self.order_id.order_line:
                record.price_unit += self.prices

    def action_cancel(self):
        pass