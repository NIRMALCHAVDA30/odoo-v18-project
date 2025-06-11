from odoo import models, api, fields # type: ignore
import random
class WizardAgent(models.TransientModel):
    _name = 'wizard.agent'
    _rec_name = "booking_id"
    
   
    booking_id = fields.Many2one("courier.booking")
    agent_id = fields.Many2one("delivery.agent")
    tracking_id = fields.Char()
    

    def action_set_agent(self):
        Booking = self.env['courier.booking']  
        active_id = self.env.context.get('active_id')
        booking_id = Booking.browse(active_id)

        for rec in self:
            booking_id.agent_id = rec.agent_id
            if not booking_id.tracking_id:
                random_number = random.randint(1000000000, 9999999999)
                print(random_number)
                booking_id.tracking_id = f"CB{random_number}"
                print(booking_id.tracking_id)
            self.env['courier.tracking'].create({
                'booking_id': booking_id.id,
                'agent_id': booking_id.agent_id.id,
                'tracking_id': booking_id.tracking_id,
            })
            
        return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'title': 'Success!',
            'message': f'Delivery Agent {rec.agent_id.name} assigned successfully.',
            'type': 'success',
            'sticky': False,
            'next': {'type': 'ir.actions.act_window_close'},
        }
    }
