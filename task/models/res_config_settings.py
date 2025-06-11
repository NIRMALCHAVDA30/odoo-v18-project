from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    vendor_bill_threshold = fields.Float(related='company_id.vendor_bill_threshold')


