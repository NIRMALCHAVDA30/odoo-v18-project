from odoo import models, fields

class RoomSeason(models.Model):
    _name = 'room.season'
    _description = 'Room Season'

    name = fields.Char(string='Season Name', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    non_refundable = fields.Boolean(string='Non-Refundable')
