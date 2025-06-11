from odoo import models, fields, api

class RestaurantOrder(models.Model):
    _name = "restaurant.order"
    _description = "Restaurant Order"
    

    # order_id = fields.Many2one("hotel.restaurant", string="Order", required=True)
    item = fields.Many2one("lunch.order",required=True)
    quantity = fields.Integer(default=1)
    unit_price = fields.Float(compute="_compute_unit_price", store=True)
    total_price = fields.Float(compute="_compute_price_total", store=True)

    #fetch the unit price
    @api.depends("item")
    def _compute_unit_price(self):
        for record in self:
            record.unit_price = record.item.price  


    @api.depends("quantity", "unit_price")
    def _compute_price_total(self):
        for record in self:
            record.total_price = record.quantity * record.unit_price
