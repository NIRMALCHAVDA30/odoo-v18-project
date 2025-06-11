from odoo import models, fields, api

class HrLeave(models.Model):
    _inherit = 'hr.leave'

    # Task : Find employees who have submitted a leave request but it hasn't been approved or refused.
    def leave_request(self):
        pending_leaves = self.env['hr.leave'].search([
            ('state', 'in', ['confirm', 'validate1','cancel'])
            ])

        print("\n\n\n\n****************>", pending_leaves)
     
        employees = pending_leaves.mapped('employee_id')
        print("\n\n\n\n>>>>>>>>>>>>>>>>>>>>", employees)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Leaves',
            'res_model': 'hr.leave',
            'view_mode': 'list,form',
            'domain': [('id', 'in', employees.ids)],
        }
