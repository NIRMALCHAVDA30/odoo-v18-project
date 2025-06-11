from odoo import models, fields, api

class MaintenanceType(models.Model):
    _name = 'maintenance.type'
    _description = 'Maintenance Type'

    name = fields.Char(required=True)
    staff_ids = fields.Many2many('staff', string="Assigned Staff")
    checklist_ids = fields.Many2many('housekeeping.checklist', string="Service")
    maintenance_service_ids = fields.One2many('maintenance.service', 'maintenance_type_id')