from odoo import fields, models

class BookRoomWizard(models.TransientModel):
    _name = "book.room.wizard"
    _description = "Book Room Wizard"

    room_id = fields.Integer()
    guest_id = fields.Integer()
    check_in_date = fields.Date()
    check_out_date = fields.Date()

    def action_button_book_room(self):
        print("\n\n\nbutton was clicked\n\n\n")
