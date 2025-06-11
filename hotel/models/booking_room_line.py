from odoo import api, models, fields

class BookingRoomLine(models.Model):
    _name = 'booking.room.line'
    _description = "Booking Room Line"
    _rec_name = "booking_id"

    booking_id = fields.Many2one('hotel.booking', string="Booking")
    room_id = fields.Many2one('room', string="Room", required=True)


    room_type = fields.Char(related='room_id.room_type_id.name', store=True)
    floor = fields.Integer(related='room_id.floor', store=True)

    check_in = fields.Date(related='booking_id.check_in_date', store=True)
    check_out = fields.Date(related='booking_id.check_out_date', store=True)

    price = fields.Float(string="Base Price", store=True)
    discount = fields.Float(string="Discount (%)", readonly=True)
    amount = fields.Float(string="Total Amount", compute="_compute_amount", store=True)

    price_rule_id = fields.Many2one('room.price', string="Price Rule")
    price_type = fields.Char(string="Price Type", readonly=True, store=True)
    

    @api.depends('room_id', 'check_in', 'check_out')
    def _compute_amount(self):
        for line in self:
            if not line.room_id or not line.check_in or not line.check_out:
                line.price = 0.0
                line.amount = 0.0
                line.discount = 0.0
                continue

            base_price = line.room_id.price_per_night
            final_amount = base_price
            discount_val = 0.0
            room_type = line.room_id.room_type_id
            hotel = line.booking_id.hotel_id 

            # Search valid room.pricelist based on date and room_type
            pricelist = self.env['room.pricelist'].search([
                ('hotel_id', '=', hotel.id),
                ('room_type_id', '=', room_type.id),
                ('valid_from', '<=', line.check_in),
                ('valid_to', '>=', line.check_out)
            ], limit=1)

            if pricelist:
                # print("\n\n\n----------PRICE LIST--", pricelist)
                
                # line.booking_id.pricee_rule_id = pricelist.id
                # print("\n\n\n->>>>>>>>>>Booking---->", line.booking_id)
                # print("\n\n\n->>>>>>>>>>Booking---->", line.booking_id.pricee_rule_id)
                line.price_rule_id = pricelist.price_id 
                line.price_type = pricelist.price_type 
                base_price = pricelist.base_price
                final_amount = pricelist.total_price

                if pricelist.price_type == 'discount':
                    if pricelist.discount_type == 'percentage':
                        discount_val = pricelist.percent_price 
                       
                    elif pricelist.discount_type == 'fixed':
                        if base_price:
                            discount_val = ((pricelist.fixed_price) / base_price) * 100
                        else:
                            discount_val = 0.0
                        
                elif pricelist.price_type == 'season':
                    if base_price:
                        increase = pricelist.increase_price
                        discount_val = -((increase / base_price) * 100)
                    else:
                        discount_val = 0.0
                    
                
                # if base_price:
                #     discount_val = (1 - final_amount / base_price) * 100

            # Set final computed values
            line.price = base_price
            line.amount = final_amount
            line.discount = discount_val

    #button add meal
    def add_meal_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Restaurant Menu',
            'res_model': 'restraunt.food', 
            'view_mode': 'kanban,form',
            'target': 'new',
            'domain': [('hotel_id', '=', self.booking_id.hotel_id.id)],  
            'context': {
                'default_booking_room_line_id': self.id,
            },
        }
    


    

