from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'


    # pump_owner = fields.Selection([
    #     ('republic_service', 'Republic Service'),
    #     ('room_cleaning_service', 'Room Cleaning Service'),
    #     ('maintenance_service', 'Maintenance Service'),
    #     ('other', 'Other')
    # ], string="Owner")


    
    pump_owner = fields.Many2one('res.partner', string="Owner", domain="[('is_owner', '=', True)]")
    is_owner = fields.Boolean("Is Owner")
    