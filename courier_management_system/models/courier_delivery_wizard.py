from odoo import models, fields, api

class CourierDeliveryWizard(models.TransientModel):
    _name = 'courier.delivery.wizard'
    _description = 'Courier Delivery Wizard'

    booking_id = fields.Many2one('courier.booking', string="Booking")
    name = fields.Many2one('res.partner' , string="Receiver's Name", required=True)
    delivery_time = fields.Datetime(string="Delivery Time", required=True, default=fields.Datetime.now)
    proof = fields.Binary(string="Proof of Delivery" , required=True)

    def action_done_delivery(self):
        print("\n\n\n\n---------->action_done_delivery")
        if self.booking_id:
            self.booking_id.receiver_id = self.name
            self.booking_id.delivery_time = self.delivery_time
            self.booking_id.delivery_proof = self.proof
          

    def action_cancel(self):
        pass
