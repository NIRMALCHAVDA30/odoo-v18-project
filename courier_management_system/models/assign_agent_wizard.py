from odoo import models, fields, api,_

class AssignAgentWizard(models.TransientModel):
    _name = 'assign.agent.wizard'
    _description = 'Assign Agent Wizard'


    booking_id = fields.Many2one('courier.booking', string="Booking")
    name = fields.Many2one('delivery.agent', required=True)
    tracking_number = fields.Char(required=True, readonly=True, copy=False, default=lambda self: _("New"))

    #sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("tracking_number", _("New")) == _("New"):
                vals["tracking_number"] = self.env["ir.sequence"].next_by_code("assign.agent.wizard") or _("New")

        return super().create(vals_list)


    #Assign agent Button
    def action_assign_agent(self):
        self.booking_id.agent_id = self.name
        self.booking_id.tracking_id = self.tracking_number
        

        self.env['courier.tracking'].create({
            'booking_id': self.booking_id.id,
            'tracking_number': self.tracking_number,
            'agent': self.name.name,
             
        })
        print("\n\n-------------->",self.booking_id )

    def action_cancel(self):
        pass




