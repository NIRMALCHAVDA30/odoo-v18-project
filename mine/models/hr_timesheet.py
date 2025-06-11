from odoo import models, api,fields
from datetime import date


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    #Task 5: Get total amount of time spent in Timesheet which has no tasks.
    def total_time_without_tasks(self):

        timesheets = self.search([('task_id', '=', False)])
        total_hours = sum(timesheets.mapped('unit_amount'))

        print(f"\n\n\nTotal hours without tasks: {total_hours}")
        return total_hours
    

    # Compute the total number of hours worked by an employee in the current month.

    def total_number_of_hours_worked_by_an_employee(self):
            employee = self.env['hr.employee'].search([])
            total_hours = {}
            for rec in employee:
                timesheet =  self.env['account.analytic.line'].search([
                    ('employee_id','=',rec.id),
                    ('date', '>=', fields.Date.today().replace(day=1)),
                    ('date', '<=', fields.Date.today())
                ])
                
                total_hours_sum = sum(record.unit_amount for record in timesheet)
                total_hours[rec.name] = { 
                    'total_hours_sum':total_hours_sum
                }
            return total_hours
            













