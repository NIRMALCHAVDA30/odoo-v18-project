from odoo import models, fields, api

class RoutePerformanceReport(models.Model):
    _name = 'route.performance.report'
    _description = 'Route Performance Report'
    _auto = False 
    _rec_name = 'route_id'

    route_id = fields.Many2one('shipping.route', string="Route", readonly=True)
    total_bookings = fields.Integer(string="Total Bookings", readonly=True)
    avg_delivery_days = fields.Float(string="Average Delivery Days", readonly=True)
    total_weight = fields.Float(string="Total Weight (Kg)", readonly=True)
    total_cost = fields.Monetary(string="Total Cost", readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency", readonly=True)

    def init(self):
        self.env.cr.execute("""
            DROP VIEW IF EXISTS route_performance_report;
            CREATE OR REPLACE VIEW route_performance_report AS (
                SELECT
                    MIN(cb.id) AS id,
                    cb.route_id,
                    COUNT(cb.id) AS total_bookings,
                    AVG(cb.delivery_estimate) AS avg_delivery_days,
                    SUM(cb.weight) AS total_weight,
                    SUM(cb.cost) AS total_cost,
                    1 AS currency_id  
                FROM
                    courier_booking cb
                WHERE
                    cb.route_id IS NOT NULL
                GROUP BY
                    cb.route_id
            )   
        """)

