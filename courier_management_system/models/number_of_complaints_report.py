from odoo import models, fields

class ComplaintStatusReport(models.Model):
    _name = 'complaint.status.report'
    _description = 'Number of open/close complaints'
    _auto = False
    _rec_name = 'status'

    status = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string="Status")

    total_complaints = fields.Integer(string="Number of Complaints")

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW complaint_status_report AS (
                SELECT
                    MIN(id) as id,
                    status,
                    COUNT(*) as total_complaints
                FROM
                    customer_complaint
                GROUP BY
                    status
            )
        """)


