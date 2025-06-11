from odoo import models, fields

class SubscriptionPlan(models.Model):
    _name = 'subscription.plan'
    _description = 'Subscription Plan'

    name = fields.Char(required=True)
    plan = fields.Integer(string="interval")
    subscription_plan_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months'),
        ('years', 'Years')
    ], required=True, string="priod")
