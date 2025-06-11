from odoo import models, fields, api
from datetime import datetime, timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # Task 7:List opportunities not converted to quotations within 14 days of creation (Archive Those Records.)
    def archive_old_unquoted_opportunities(self):
        cutoff_date = fields.Datetime.now() - timedelta(days=14)

        
        leads_to_archive = self.search([
            ('type', '=', 'opportunity'),
            ('create_date', '<=', cutoff_date),
            ('active', '=', True),
        ])
        print("\n\n\n===================>", leads_to_archive)

       
        leads_to_archive.write({'active': False})

        print(f"\n\n\n--------------------> {len(leads_to_archive)}")
        return True
    
    #Task: Find Salesperson with 10% and more probability of oppurtunity
    def salesperson_with_10_and_more_probability(self):
        probability = self.env['crm.lead'].search([
            ('probability', '>=', 10)
        ]).mapped('user_id')

        print("\n\n\n---------probability------>",probability.mapped('name'),"\n\n\n")

