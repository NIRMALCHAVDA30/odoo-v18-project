from odoo import models, fields, api
from datetime import timedelta, date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    #Archive employees whose contracts ended over 6 months ago.
    #in the install the hr_contract module
    contracts_ended = date.today() - timedelta(days=180)
    print("\n\n\n\n-----contracts_ended--->", contracts_ended)

    def employee_whose_contracts_ended(self):
        employees = self.env['hr.contract'].search([
        ('date_end', '<', self.contracts_ended),
        ('active', '=', True)
    ])
        
        print("\n\n\n\n-------employees---->", employees.mapped('employee_id.name'))
        employees.write({'active': False})

        print(f"\n\n\n---------Archive employees-----------> {len(employees)}")


