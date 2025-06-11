from odoo import api, models, fields


class HotelManagement(models.Model):
    _name = "hotel.management"
    _description = "This is the hotel management module"

    name = fields.Char(string="Hotel Name", required=True)
    location = fields.Text()
    contact = fields.Char()
    description = fields.Text()
    hotel_image = fields.Image()

    room_ids = fields.One2many("hotel.room", "hotel_id")

    # state button for available room
    available_room_count = fields.Integer(
        string="Available Rooms", compute="_compute_available_rooms"
    )

    @api.depends("room_ids", "room_ids.is_available")
    def _compute_available_rooms(self):
        for hotel in self:
            hotel.available_room_count = len(hotel.room_ids.filtered(lambda a: a.is_available))

    def action_view_available_rooms(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Available Rooms",
            "res_model": "hotel.room",
            "view_mode": "list,form",
            "domain": [("is_available", "=", True), ("hotel_id", "=", self.id)],  #linked to the current hotel
            "context": {"default_hotel_id": self.id},
        }
    
    #state button for booked room
    available_book_room_count = fields.Integer(string="Booked Rooms", compute="_compute_book_rooms")

    @api.depends("room_ids")
    def _compute_book_rooms(self):
        for hotel in self:
            hotel.available_book_room_count = len(hotel.room_ids.filtered(lambda a: a.is_available==False))

    def action_view_book_rooms(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Book Rooms",
            "res_model": "hotel.room",
            "view_mode": "list,form",
            "domain": [("is_available", "=", False), ("hotel_id", "=", self.id)],  #linked to the current hotel
            "context": {"default_hotel_id": self.id},
        }
    
    #Book now button
    def action_book_now(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Select Guest",
            "res_model": "res.partner", 
            "view_mode": "kanban,list,form",  
            "domain": [], 
            "context": {"default_is_company": False},  # Default as individual
        }

