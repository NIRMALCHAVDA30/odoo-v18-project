from odoo import api, models, fields
from odoo.exceptions import ValidationError
import re

class Partner(models.Model):
    _inherit = "res.partner"

    @api.constrains("phone")
    def _check_phone(self):
        for record in self:
            if record.phone:
                if not record.phone.isdigit():
                    raise ValidationError("Phone number only digits.")
                if len(record.phone) !=10:
                    raise ValidationError("Phone number only 10 digits.")
                
    @api.constrains("email")
    def _check_email(self):
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        for record in self:
            if record.email and not re.match(email_regex , record.email):
                raise ValidationError("Invalid email format. Please enter the valid email address.")