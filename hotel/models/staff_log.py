from odoo import models, fields, api

class StaffLog(models.Model):
    _name = 'staff.log'
    _description = 'Staff Check-in / Check-out'
    _rec_name = 'staff_id'

    staff_id = fields.Many2one('staff', string="Staff", required=True)
    check_in = fields.Datetime(string="Check-In Time", required=True)
    check_out = fields.Datetime(string="Check-Out Time")