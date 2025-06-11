from odoo import models, fields, api, _

class HousekeepingRequest(models.Model):
    _name = "housekeeping.request"
    _description = "Housekeeping Request"

    #sequence
    name = fields.Char(
        required=True, readonly=True, copy=False, default=lambda self: _("New")
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("housekeeping.request") or _("New") 

        return super().create(vals_list)
    


    room_id = fields.Many2one("hotel.room" , required=True)
    description = fields.Text()
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent to Housekeeping'),
        ('assigned', 'Assigned to Staff'),
        ('completed', 'Completed')
    ], default='draft')


    def action_send_to_housekeeping(self):
        housekeeping_request = self.env['hotel.housekeeping'].create({
            'request_id': self.id,
            'room_id': self.room_id.id,
            'description': self.description,
        })

        self.status = 'sent'

        # return {
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'hotel.housekeeping',
        #     'view_mode': 'list,form',
        #     'res_id': housekeeping_request.id,
        #     'target': 'current',
        # }

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Request Sent Notification',
                'type': 'success',
                'message': "Request sent to housekeeping successfully!!",
                'next': {'type': 'ir.actions.act_window_close'},
            }
        }
    
        

