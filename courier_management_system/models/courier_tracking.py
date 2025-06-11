from odoo import models, fields

class CourierTracking(models.Model):
    _name = 'courier.tracking'
    _description = 'Courier Tracking'
    _inherit = ['mail.thread']
    _rec_name = 'booking_id'
    _inherits = {'courier.booking': 'booking_id'}


    booking_id = fields.Many2one('courier.booking', string='Tracked Courier')
    timestamp = fields.Datetime(default=fields.Datetime.now)
    notes = fields.Text()
    tracking_number = fields.Char()
    agent = fields.Char()


    def action_pickup(self):
        for rec in self:
             if rec.booking_id:
                  rec.booking_id.status = 'picked'
                  rec.status = 'picked'
                  rec.booking_id.pickup_time = fields.Datetime.now()

    def action_in_transit(self):
        for rec in self:
            if rec.booking_id:
                rec.booking_id.status = 'in_transit'
                rec.status = 'in_transit'

    def action_out_for_delivery(self):
        for rec in self:
            if rec.booking_id:
                rec.booking_id.status = 'out_for_delivery'
                rec.status = 'out_for_delivery'

    def action_delivered(self):
        print("button cicked \n\n\n\n")
        for rec in self:
            if rec.booking_id:
                rec.booking_id.status = 'delivered'
                rec.status = 'delivered'

        return {
            'name': 'Assign Delivery Agent',
            'type': 'ir.actions.act_window',
            'res_model': 'courier.delivery.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_booking_id': self.booking_id.id
            }
        }
        
