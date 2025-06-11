from odoo import models, api, fields # type: ignore
from odoo.exceptions import UserError

class DeliveryAgent(models.Model):
    _name = 'delivery.agent'
    _rec_name ="user_id" 
    

    partner_id = fields.Many2one('res.partner', ondelete="cascade")
    name = fields.Char(string="Name")
    user_id = fields.Many2one("res.users")
    is_available =  fields.Selection(
        selection=[('on_track', 'Available'), ('off_track', 'Not Available')],
         default='off_track', tracking=True
    )
    agent_phone = fields.Char()
    
    @api.constrains('agent_phone')
    def _check_phone(self):
        for rec in self:
            if rec.agent_phone:
                if not rec.agent_phone.isdigit():
                    raise UserError("Phone number must contain only digits.")
                if len(rec.agent_phone) != 10 and len(rec.agent_phone) > 0:
                    print(len(rec.agent_phone))
                    raise UserError("Phone number must be exactly 10 digits long.")