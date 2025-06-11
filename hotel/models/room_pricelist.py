from odoo import models, fields, api
from odoo.exceptions import ValidationError

class RoomPricelist(models.Model):
    _name = 'room.pricelist'
    _description = 'Room Pricelist'
    _rec_name = 'price_type'


    price_id = fields.Many2one('room.price', required=True)

    hotel_id = fields.Many2one('hotel', required=True, related='price_id.hotel_id')
    # room_id = fields.Many2one('room', required=True)
    room_type_id = fields.Many2one('room.type', string='Room Type', required=True)
    
    base_price = fields.Float(string='Base Price', required=True, related='room_type_id.price')

    price_type = fields.Selection([
        ('season', 'Season'),
        ('discount', 'Discount')
    ], required=True)

    # Season
    season_id = fields.Many2one('room.season', string='Season')
    increase_price = fields.Float(string='Increase Price')
    valid_from = fields.Date(related='season_id.start_date' , readonly=False, store=True, required=True)
    valid_to = fields.Date(related='season_id.end_date', readonly=False, store=True, required=True)


    # Discount
    discount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage')
    ], string='Discount Type')

    fixed_price = fields.Float(string="Fixed Price")
    percent_price = fields.Float(string="Percentage Discount")


    total_price = fields.Float(string='Total Price', compute='_compute_total_price', store=True)

    @api.depends('price_type', 'base_price', 'increase_price', 'discount_type', 'fixed_price', 'percent_price')
    def _compute_total_price(self):
        for rec in self:
            if rec.price_type == 'season' and rec.increase_price:
                rec.total_price = rec.base_price + rec.increase_price

            elif rec.price_type == 'discount':
                if rec.discount_type == 'fixed':
                    rec.total_price = max(0, rec.base_price - rec.fixed_price)
                elif rec.discount_type == 'percentage':
                    rec.total_price = max(0, rec.base_price * (1 - (rec.percent_price / 100)))
                else:
                    rec.total_price = rec.base_price
            else:
                rec.total_price = rec.base_price



    @api.constrains('hotel_id', 'room_type_id', 'valid_from', 'valid_to')
    def _check_set_pricelist(self):
        for record in self:
            set = self.search([
                ('id', '!=', record.id),
                ('hotel_id', '=', record.hotel_id.id),
                ('room_type_id', '=', record.room_type_id.id),
                ('valid_from', '<=', record.valid_to),
                ('valid_to', '>=', record.valid_from),
            ])
            if set:
                raise ValidationError(
                    "A pricelist for this room type and hotel already exists for the selected date range."
                )
