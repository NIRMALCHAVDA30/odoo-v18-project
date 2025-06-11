from odoo import models, fields, api

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'


    #Task 5
    total_time = fields.Float(compute="_total_time_spent", store=True)

    @api.depends('task_id')
    def _total_time_spent(self):
        for record in self:
            if not record.task_id:
                record.total_time = sum(record.mapped("unit_amount"))
                print("\n\n\n-----TOTAL TIME->", record.total_time)             
