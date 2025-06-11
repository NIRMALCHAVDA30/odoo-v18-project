from odoo import models, api, fields # type: ignore
from odoo.exceptions import UserError
from datetime import datetime,date


class CourierTracking(models.Model):
    _name = 'courier.tracking'
    _inherits = {'courier.booking': 'booking_id'}
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "booking_id"
    
    name = fields.Char(compute="_compute_name")
    booking_id = fields.Many2one("courier.booking")
    timestamp = fields.Datetime(
    default=date.today())
    
    @api.depends('booking_id')
    def _compute_name(self):
        for record in self:
            record.name = record.booking_id.booking_sequence
        
    def action_pickup(self):
        for rec in self:
            if not rec.invoice_ids:
                raise UserError('Still Invoice Is Not Generated Wait For It.')
            else:
                rec.state = 'picked'
                rec.timestamp = datetime.now()
                rec.pickup_time = rec.timestamp
    
    def action_in_transit_time(self):
        for rec in self:
            rec.state = 'in_transit'
            rec.in_transit_time = datetime.now()
    
    def action_out_for_delivery(self):
        for rec in self:
            rec.state = 'out_for_delivery'
            rec.out_for_delivery_time = datetime.now()
            rec.rating = rec.booking_id.rating

    def action_btn_delivered(self):
        for rec in self:
            rec.state = 'delivered'
            rec.delivered_time = datetime.now()
            return {
                'name': 'Delivery Details',
                'type': 'ir.actions.act_window',
                'res_model': 'courier.booking',
                'res_id': rec.booking_id.id, 
                'target': 'new',
                'view_id': self.env.ref('courier_management.courier_delivery_wizard_form_view').id,
                'view_mode': 'form',
            }

    def action_view_complaints(self):
        self.ensure_one()
        if self.complaint_ids:
             return {
                "type": "ir.actions.act_window",
                "res_model": "customer.complaint",
                "view_mode": "list,form",
                "res_id": self.complaint_ids[0].id,
                "target": "current",
            }
        else:
            raise UserError("No Complaints Found For This Courier.")
