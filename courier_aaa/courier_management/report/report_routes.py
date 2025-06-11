from odoo import fields, models

class report_routes(models.Model):
    _name = 'report.routes'
    _description = 'Contains Reports for shipping routes model'
    _auto = False
    
    state = fields.Selection(
        selection = [('draft','Draft'),('confirmed','Confirmed'),('invoiced','Invoiced'),('picked','Picked'),
                     ('in_transit','In Transit'),('out_for_delivery','Out For Delivery'),('delivered','Delivered')
                    ])
    
    booking_id = fields.Many2one('courier.booking')
    count = fields.Integer()
    route_id = fields.Many2one("shipping.route")
    booking_route_id = fields.Many2one('shipping.route')
    def _select_fields(self):
        select_ = f'''
        COUNT(courier_booking.id) AS count,
        courier_booking.id AS booking_id,
        courier_booking.state AS state,
        courier_booking.route_id AS booking_route_id,
        shipping_route.id AS shipping_route_id
        '''
        return select_
    
    def _from_model(self):
        return f'''
        courier_booking,
        shipping_route
        '''
    def _where_condition(self):
        return '''
        courier_booking.route_id = shipping_route.id
        '''
        
    def _group_by_route(self):
        return '''
        courier_booking.id,
        courier_booking.state,
        courier_booking.route_id,
        shipping_route.id
        '''
        
    def _query(self):
        return f'''
            SELECT {self._select_fields()}
            FROM {self._from_model()}
            WHERE {self._where_condition()}
            GROUP BY {self._group_by_route()}
        '''
        
    @property
    def _table_query(self):
        return self._query()
    
    