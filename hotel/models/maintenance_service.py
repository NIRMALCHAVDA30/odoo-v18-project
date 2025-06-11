from odoo import models, fields, api

class MaintenanceService(models.Model):
    _name = 'maintenance.service'
    _description = 'Maintenance Service'
    _rec_name = 'maintenance_type_id'

    maintenance_date = fields.Date(required=True, default=fields.Date.today)
    staff_id = fields.Many2many('staff.log', required=True)
    maintenance_type_id = fields.Many2one('maintenance.type', required=True)
    checklist_ids = fields.Many2many('housekeeping.checklist')
    room_id = fields.Many2one('room', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], default='draft')


    