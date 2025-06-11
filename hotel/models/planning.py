from odoo import models, fields, api

class Planning(models.Model):
    _name = 'planning'
    _description = 'Planning'

    name = fields.Char(required=True)
    staff_id = fields.Many2one('staff.log', required=True)
    maintenance_type_id = fields.Many2one('maintenance.type',required=True)
    room_ids = fields.Many2many('room', string='Rooms')
