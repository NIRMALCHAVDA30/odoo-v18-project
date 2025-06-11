from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Staff(models.Model):
    _name = 'staff'
    _description = 'Housekeeping Staff'

    name = fields.Char(string='Staff Name')
    email = fields.Text()
    phone = fields.Char()
    job_position = fields.Char(default='Housekeeping')
    staff_photo = fields.Image()
    age = fields.Integer()

    @api.constrains('age')
    def _check_age(self):
        for record in self:
            if record.age < 18:
                raise ValidationError("Staff age must be at least 18 years.")
