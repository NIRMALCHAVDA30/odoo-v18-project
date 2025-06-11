from odoo import models, api, fields # type: ignore
from odoo.exceptions import UserError # type: ignore
from datetime import date, timedelta

class CourierCategory(models.Model):
    _name = "courier.category"
    _description = "Courier Category"
    
    name = fields.Char()
    color = fields.Integer()
    _sql_constraints =[('tag_unique','UNIQUE(name)','The Category Name Must be Unique')]