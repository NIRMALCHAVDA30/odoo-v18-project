from odoo import api, models, fields
from odoo import Command
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_sales = fields.Many2one("sale.order")

    @api.onchange("x_sales")
    def _onchange_x_sales(self):
        if self.x_sales:
            self.partner_id = self.x_sales.partner_id
            print("<<<<<<<<<<<<,SALES:" , self.x_sales) 
            print("\n\n\n>>>>>>>>>>>>>PARTNER ID :",self.partner_id)
            # self.order_line = self.x_sales.order_line


            # self.order_line = [
            #     Command.create({
            #         'product_id': line.product_id.id,
            #         'product_uom_qty': line.product_uom_qty,
            #         'price_unit': line.price_unit,
            #     }) for line in self.x_sales.order_line
            # ]


            # order_line_updates = [(5, 0, 0)]  #unlink all
            # order_line_updates += [
            #     (0, 0 , {
            #         'product_id': line.product_id.id,
            #         'product_uom_qty':line.product_uom_qty,
            #         'price_unit': line.price_unit,
            #     })for line in self.x_sales.order_line
            # ]

            # self.order_line = order_line_updates 


            # order_line_updates = [(6, 0, [])]  #replace 
            # order_line_updates += [
            #     (0, 0 , {
            #         'product_id': line.product_id.id,
            #         'product_uom_qty':line.product_uom_qty,
            #         'price_unit': line.price_unit,
            #     })for line in self.x_sales.order_line
            # ]

            # self.order_line = order_line_updates 
            

            self.order_line = [(6, 0, [line.id for line in self.x_sales.order_line])]


    # #button action
    # def action_button(self):
    #     raise ValidationError("You Can't click on button :)")


    # state = fields.Selection(
    #     selection=[
    #         ("draft", "Quotation"),
    #         ("sent", "Quotation Sent"),
    #         ("sale", "Sales Order"),
    #         ("cancel", "Cancelled"),
    #         ("done", "Sale Order Done"),
    #     ],
    #     string="Status",
    # )
            
            
   
