from odoo import models, fields, api
from datetime import date

class ProjectTask(models.Model):
    _inherit = 'project.task'

    # Task: Get open tasks without user assignment.
    def open_tasks_without_user_assignment(self):
        tasks = self.env['project.task'].search([
        ("is_closed", "=", False),
        ("user_ids", "=", False)
        ])

        return {
                'type': 'ir.actions.act_window',
                'name': 'Open tasks without user assignment',
                'res_model': 'project.task',
                'view_mode': 'list,form',
                'domain': [('id', 'in', tasks.ids)],
            }
    

    # Compute the average task completion time per project.
    def average_task(self):
        projects = self.env['project.project'].search([])
        result = {}
        for rec in projects:
            print("\n\n\n<<<<<< Rec ----------->", rec)
            tasks = self.env['project.task'].search([
                ('project_id', '=', rec.id),
                ('date_deadline', '!=', False),
                ('create_date', '!=', False)
            ])

            durations = []
            for record in tasks:
                if record.date_deadline and record.create_date:

                    deadline_date = record.date_deadline.date()
                    created_date = record.create_date.date()

                    days_difference = (deadline_date - created_date).days

                    durations.append(days_difference)


            print("\n\n\n<<<<<< durations ----------->", durations)

            if durations:
                average_days = sum(durations) / len(durations)
            else:
                average_days = 0
            
            result[rec] = average_days
            print("\n\n\n<<<<<< RESULT ----------->", result[rec])



    # Task : List all Tasks that delayed the deadline and still on ‘New’ State.
    today = fields.Date.today()

    def tasks_delayed_the_deadline(self):
        delayed_tasks = self.env['project.task'].search([
            ('date_deadline', '<', self.today),
            ('stage_id.name', '=', 'New')
        ])

        print("\n\n\n------delayed_tasks------->", delayed_tasks.mapped('name'))

        return {
                'type': 'ir.actions.act_window',
                'name': 'Delayed Tasks',
                'res_model': 'project.task',
                'view_mode': 'list,form',
                'domain': [('id', 'in', delayed_tasks.ids)],
            }
    












