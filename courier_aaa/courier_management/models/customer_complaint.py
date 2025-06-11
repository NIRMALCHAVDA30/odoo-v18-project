from odoo import models, api, fields # type: ignore
from odoo.exceptions import UserError
import random
from datetime import timedelta, date

class CustomerComplaint(models.Model):
    _name = 'customer.complaint'
    _inherits = {'courier.booking': 'booking_id'}
    _rec_name = "booking_id"
    _inherit = ['mail.thread', 'mail.activity.mixin']
 

    name = fields.Char(compute="_compute_name")
    booking_id = fields.Many2one("courier.booking" ,required=True)
    complaint_category = fields.Selection(
        string='Complaint Category',
        selection=[('delay', 'Delay'), ('wrong_delivery', 'Wrong Delivery'),('payment_issue','Payment Issue')],required=True)
    partner_id  = fields.Many2one("res.partner",default=lambda self:self.env.user.partner_id.id)
    description = fields.Text(required=True)
    attachment = fields.Binary()
    ticket_number = fields.Char()
    assigned_to = fields.Many2one("res.users")
    status = fields.Selection(
       selection=[('open', 'Open'), ('in_progress', 'In Progress'),('resolved','Resolved'),('closed','Closed')],default="open")
    priority = fields.Selection(
       selection=[('low', 'Low'), ('medium', 'Medium'),('high','High')],compute="_compute_complaint_categ",default="low"
    )
    resolution_deadline = fields.Date()
    internal_notes = fields.Text()
    
    @api.depends('name')
    def _compute_name(self):
        for record in self:
            record.name = record.booking_id
    
    
    @api.depends('complaint_category')
    def _compute_complaint_categ(self):
        for rec in self:
            if rec.complaint_category == 'delay':
                rec.priority = 'low'
            elif rec.complaint_category == 'wrong_delivery':
                rec.priority = 'medium'
            elif rec.complaint_category == 'payment_issue':
                rec.priority = 'high'

    def action_set_in_progress(self):
        for rec in self:
            rec.status = 'in_progress'

    def action_set_resolved(self):
        for rec in self:
            rec.status = 'closed'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success!',
                'message': f'Complaint Has Been Closed of Ticket Id:{rec.ticket_number}.',
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Your Complaint Has Been Closed.',
                    'type': 'rainbow_man',
                }
            }
        }

    def action_complaint_create(self):
        for rec in self:
            random_number = random.randint(1000000000, 9999999999)
            rec.ticket_number = f"Ticket-{random_number}"
            print(rec.ticket_number)

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Success!',
                'message': f'Complaint has been created with No. {rec.ticket_number}.',
                'type': 'success',
                'sticky': False,
                'next': {'type': 'ir.actions.act_window_close'},
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Ticket Created Successfully!',
                    'type': 'rainbow_man',
                }
            }
        }
