from odoo import fields, models

class report_agent(models.Model):
    _name = 'report.agent'
    _description = 'Contains Reports for agent based on complaint category model'
    _auto = False
    
    complaint_category = fields.Selection(
        string='Complaint Category',
        selection=[('delay', 'Delay'), ('wrong_delivery', 'Wrong Delivery'),('payment_issue','Payment Issue')]
    )
    
    booking_id = fields.Many2one('courier.booking')
    
    count = fields.Integer()
    
    complaints_booking_id = fields.Many2one('courier.booking')
    
    agent_id = fields.Many2one("delivery.agent")
    
    def _select_fields(self):
        select_ = f'''
        COUNT(courier_booking.id) AS count,
        courier_booking.id AS booking_id,
        courier_booking.agent_id AS agent_id,
        customer_complaint.complaint_category AS complaint_category,
        customer_complaint.booking_id AS complaints_booking_id
        '''
        return select_
    
    def _booking_model(self):
        return f'''
        courier_booking
        '''
    
    def _complaints_model(self):
        return f'''
        customer_complaint
        '''
    
    def _on_condition(self):
        return '''
        courier_booking.id = customer_complaint.booking_id
        '''
        
    def _group_by_complaints(self):
        return '''
        courier_booking.id,
        customer_complaint.booking_id,
        customer_complaint.complaint_category,
        courier_booking.agent_id
        '''
        
    def _query(self):
        return f'''
            SELECT {self._select_fields()}
            FROM {self._booking_model()}
            JOIN {self._complaints_model()}
            ON {self._on_condition()}
            GROUP BY {self._group_by_complaints()}
        '''
        
    @property
    def _table_query(self):
        return self._query()
    