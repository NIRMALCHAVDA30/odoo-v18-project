from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    #Task :  Detect stock moves where source and destination locations are the same.
    # in the inventory module Inventory>Reporting>Moves Analysis
    def action_source_destination_location(self):

        same_location_moves =  self.env['stock.move'].search([]).filtered(
            lambda m: m.location_id.id == m.location_dest_id.id
        )
        print("\n\n\n----------->",same_location_moves )



