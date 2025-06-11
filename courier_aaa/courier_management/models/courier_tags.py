from odoo import models, api, fields # type: ignore

class CourierTags(models.Model):
    _name = 'courier.tags'
    _order = "name"
    
    name = fields.Char()
    color = fields.Integer()
    
    _sql_constraints =[('tag_unique','UNIQUE(name)','The Tag Name Must be Unique')]