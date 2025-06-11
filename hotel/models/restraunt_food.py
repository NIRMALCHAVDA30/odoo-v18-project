from odoo import models, fields, api

class RestrauntFood(models.Model):
    _name = 'restraunt.food'
    _description = 'Food (Restaurant Item)'

    name = fields.Char(string="Food Name", required=True)
    description = fields.Text(string="Description")

    food_image = fields.Image()
    
    restaurant_id = fields.Many2one('restaurant', string="Restaurant")
    hotel_id = fields.Many2one('hotel', related='restaurant_id.hotel_id', store=True)
    price = fields.Float()

    # def action_order(self):
    #     print("\n\n\n\n----Button was clicked")
    #     pass
        # booking_line_id = self.env.context.get('default_booking_room_line_id')
        # if booking_line_id:
        #     booking = self.env['booking.room.line'].browse(booking_line_id)
        #     booking.write({
        #         'selected_food_ids': [(4, self.id)]
        #     })


    def action_order(self):
        booking_line_id = self.env.context.get('default_booking_room_line_id')
        print("\n\n\n\n-----------", booking_line_id)
        if booking_line_id:
            booking_line = self.env['booking.room.line'].browse(booking_line_id)
            booking = booking_line.booking_id  

            # Check if already ordered
            already_ordered = self.env['restraunt.order'].search([
                ('booking_id', '=', booking.id),
                ('food_id', '=', self.id)
            ])
            if not already_ordered:
                self.env['restraunt.order'].create({
                    'booking_id': booking.id,
                    'food_id': self.id
                })






    
