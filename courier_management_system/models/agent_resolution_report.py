from odoo import models, fields

class AgentResolutionReport(models.Model):
    _name = 'agent.resolution.report'
    _description = 'Agent-wise Complaint Resolution Report'
    _auto = False
    _rec_name = 'agent_id'

    agent_id = fields.Many2one('res.users', string='Agent')
    complaint_category = fields.Selection([
        ('delay', 'Delay'),
        ('damage', 'Damage'),
        ('wrong_delivery', 'Wrong Delivery'),
        ('payment_issue', 'Payment Issue'),
        ('other', 'Other'),
    ])
    resolved_count = fields.Integer(string='Resolved Complaints')

    def init(self):
        self.env.cr.execute("""
            DROP VIEW IF EXISTS agent_resolution_report;           
            CREATE OR REPLACE VIEW agent_resolution_report AS (
                SELECT
                    MIN(id):: BIGINT AS id,
                    assigned_to AS agent_id,
                    complaint_category,
                    COUNT(*) AS resolved_count
                FROM customer_complaint
                GROUP BY assigned_to,complaint_category
            )
        """)