from odoo import models, fields

class SaleCancelReason(models.Model):
    _name = 'sale.cancel.reason'
    _description = 'Sale Cancel Reason'

    name = fields.Char(required=True)
