from odoo import models, fields, api
from datetime import date, timedelta

class MailActivity(models.Model):
    _inherit = 'mail.activity'


    # Task : Archive partners with no activity in the past 2 years
    # Setting>Technical>Activity Overview
    cutoff_date = date.today() - timedelta(days=730)

    def hello(self):
        partners = self.env['res.partner'].search([
            ('activity_ids', '=', False),
            ('write_date', '<', self.cutoff_date),
            ])
        print("----------------partners--------->", partners.mapped('name'))

        partners.write({'active' : False})

        

        