from odoo import api, models, fields
from odoo.exceptions import ValidationError

class Guest(models.Model):
    _name = "guest"
    _description = "Hotel Guest"

    name = fields.Char()
    phone = fields.Char(required=True, size=10)
    aadhaar_id = fields.Char(required=True, size=12)
    pan_card = fields.Char(required=True, size=8)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ])

    guest_image = fields.Image()
    upload_adhar = fields.Image()
    

    @api.constrains('phone', 'aadhaar_id')
    def _check_guest_fields(self):
        for rec in self:
            # Phone
            if not rec.phone.isdigit() or len(rec.phone) != 10:
                raise ValidationError("Phone number must be exactly 10 digits.")

            # Aadhaar
            if not rec.aadhaar_id.isdigit() or len(rec.aadhaar_id) != 12:
                raise ValidationError("Aadhaar ID must be exactly 12 digits.")
