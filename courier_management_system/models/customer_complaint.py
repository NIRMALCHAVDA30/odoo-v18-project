from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class CustomerComplaint(models.Model):
    _name = 'customer.complaint'
    _description = 'Customer Complaint'
    _inherit = ['mail.thread']
    _rec_name = 'booking_id'

    booking_id = fields.Many2one('courier.booking', required=True)
    complaint_category = fields.Selection([
        ('delay', 'Delay'),
        ('damage', 'Damage'),
        ('wrong_delivery', 'Wrong Delivery'),
        ('payment_issue', 'Payment Issue'),
        ('other', 'Other'),
    ], required=True)
    description = fields.Text(string="Complaint Detail")
    attachment = fields.Binary(string="Attachment")
    ticket_number = fields.Char(string="Ticket Number", copy=False)
    assigned_to = fields.Many2one('res.users', string="Assigned To")
    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], default='open', tracking=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    resolution_deadline = fields.Date()
    internal_notes = fields.Text()

    #sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("ticket_number", _("New")) == _("New"):
                vals["ticket_number"] = self.env["ir.sequence"].next_by_code("customer.complaint") or _("New")

        return super().create(vals_list)
    

    @api.onchange('assigned_to')
    def _onchange_assigned_to(self):
        for record in self:
            if record.assigned_to:
                record.status = 'in_progress'
            else:
                record.status = 'open'

    #Resolve button
    def action_resolve(self):
        for record in self:
            if not record.assigned_to or not record.resolution_deadline:
                raise ValidationError("Must fill both 'Assigned To' and 'Resolution Deadline' before resolving.")
            record.status = 'resolved'

    #Close button
    def action_close(self):
        for record in self:
            record.status = 'closed'



    @api.constrains('resolution_deadline')
    def _check_resolution_deadline(self):
        for record in self:
            today = fields.Date.today()
            if record.resolution_deadline < today:
                raise ValidationError("Resolution Deadline must be a future date.")


