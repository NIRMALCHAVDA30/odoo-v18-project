from odoo import fields, models

class report_modes(models.Model):
    _name = 'report.modes'
    _description = 'Contains Reports for modes model'
    _auto = False
    
    selected_mode_id = fields.Many2one('shipping.mode')
    state = fields.Selection(
        selection = [('draft','Draft'),('confirmed','Confirmed'),('invoiced','Invoiced'),('picked','Picked'),
                     ('in_transit','In Transit'),('out_for_delivery','Out For Delivery'),('delivered','Delivered')
                    ])
    
    booking_id = fields.Many2one('courier.booking')
    
    cost = fields.Float(string="Cost")
    
    count = fields.Integer()
    
    shipping_mode_id = fields.Many2one('shipping.mode')
    
    def _select_fields(self):
        select_ = f'''
        COUNT(courier_booking.id) AS count,
        courier_booking.id AS booking_id,
        courier_booking.cost AS cost,
        courier_booking.state AS state,
        courier_booking.selected_mode_id AS selected_mode_id,
        shipping_mode.id AS shipping_mode_id
        '''
        
        return select_
    
    def _from_model(self):
        return f'''
        courier_booking,
        shipping_mode
        '''
    def _where_condition(self):
        return '''
        courier_booking.selected_mode_id = shipping_mode.id
        '''
        
    def _group_by_mode(self):
        return '''
        courier_booking.id,
        courier_booking.state,
        courier_booking.cost,
        courier_booking.selected_mode_id,
        shipping_mode.id
        '''
        
    def _query(self):
        return f'''
            SELECT {self._select_fields()}
            FROM {self._from_model()}
            WHERE {self._where_condition()}
            GROUP BY {self._group_by_mode()}
        '''
        
    @property
    def _table_query(self):
        return self._query()
    
    