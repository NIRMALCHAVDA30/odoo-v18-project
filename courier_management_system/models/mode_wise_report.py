from odoo import models, fields, api


class ModeWiseReport(models.Model):
    _name = 'mode.wise.report'
    _description = 'Mode Wise Report'
    _auto = False  
    _rec_name = 'mode_id'

    mode_id = fields.Many2one('shipping.mode', string="Mode", readonly=True)
    total_bookings = fields.Integer(string="Total Bookings", readonly=True)
    total_weight = fields.Float(string="Total Weight (kg)", readonly=True)
    total_cost = fields.Monetary(string="Total Cost", readonly=True)
    currency_id = fields.Many2one('res.currency', readonly=True)

    def _query(self):
        return """
            SELECT
                MIN(cb.id) AS id,
                cb.selected_mode_id AS mode_id,
                COUNT(cb.id) AS total_bookings,
                SUM(cb.weight) AS total_weight,
                SUM(cb.cost) AS total_cost,
                cb.currency_id 
            FROM courier_booking cb
            WHERE cb.selected_mode_id IS NOT NULL
            GROUP BY cb.selected_mode_id, cb.currency_id
        """


    @property
    def _table_query(self):
        return self._query()
