from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pump_owner = fields.Many2one('res.partner', string='Owner', compute='_compute_pump_owner', store=True)

    @api.depends('partner_shipping_id', 'partner_shipping_id.pump_owner', 'partner_shipping_id.is_owner')
    def _compute_pump_owner(self):
        for record in self:
            print("\n\n\n---------->",record)
            if record.partner_shipping_id:
                if record.partner_shipping_id.is_owner:
                    record.pump_owner = record.partner_shipping_id
                elif record.partner_shipping_id.pump_owner:
                    record.pump_owner = record.partner_shipping_id.pump_owner
                else:
                    record.pump_owner = False
            else:
                record.pump_owner = False


    

