from odoo import models, fields

class HousekeepingChecklist(models.Model):
    _name = 'housekeeping.checklist'
    _description = 'Housekeeping Checklist'

    name = fields.Char()