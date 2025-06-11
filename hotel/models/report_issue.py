from odoo import models, fields, api

class ReportIssue(models.Model):
    _name = 'report.issue'
    _description = 'Report Room Issues'
    _rec_name = 'room_id'

    guest_id = fields.Many2one('guest',required=True)
    staff_id = fields.Many2one('staff', string="Resolved By")
    hotel_id = fields.Many2one('hotel', required=True)
    room_id = fields.Many2one('room', required=True)
    issue_description = fields.Text(required=True)
    solution = fields.Text()
    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], default='draft', string="Status", required=True)


    # Button Send Report
    def action_send_report(self):
        for rec in self:
            rec.status = 'in_progress'

    # Button Resolved
    def action_resolved(self):
        for rec in self:
            rec.status = 'resolved'