from odoo import models, fields

class TypeWiseReportComplaint(models.Model):
    _name = 'type.wise.report.complaint'
    _description = 'Complaint Type Report'
    _auto = False 
    _rec_name = 'complaint_category'

    complaint_category = fields.Selection([
        ('delay', 'Delay'),
        ('damage', 'Damaged'),
        ('wrong_delivery', 'Wrong Delivered'),
        ('payment_issue', 'Payment Issue'),
        ('other', 'Other')
    ], string="Complaint Category")

    complaint_count = fields.Integer(string="Number of Complaints")

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW type_wise_report_complaint AS (
                SELECT
                    MIN(id) AS id,
                    complaint_category,
                    COUNT(*) AS complaint_count
                FROM customer_complaint
                GROUP BY complaint_category
            )
        """)





