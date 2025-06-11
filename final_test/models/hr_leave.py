from odoo import models, fields, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

   
    def leave_request(self):
        print("\n\n\n-------->")
        leave = self.env['hr.leave'].search([
            ('state', 'in', ['confirm','validate1','cancel'])
        ])
        employees = leave.mapped('employee_id')
        print("\n\n\n>>>>>>>>>>>", employees.name)
        return employees.name



