from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    vendor_bill_threshold = fields.Float(string="Vendor Bill Threshold Limit")