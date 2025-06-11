from odoo import models, fields

class HotelPartner(models.Model):
    _inherit = 'res.partner'
    
    is_guest = fields.Boolean(string="Is a Hotel Guest?", default=False)
    id_proof = fields.Char(required=True, string="Identity proof")
    nationality = fields.Many2one("res.country")
    preferences = fields.Text(string="Guest preferences")

    def action_open_reservation_form(self):
        return {
            'name': 'Create Reservation',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.reservation',
            'view_mode': 'form',
            'view_id': self.env.ref('hotel_management_system.hotel_reservation_view_form').id,
            'target': 'new', 
            'context': {
                'default_partner_id': self.id,  # Auto-fill guest field
            },
        }
    
    #state button Reservation history
    reservation_count = fields.Integer(compute="_compute_reservation_count", string="Reservations")

    def _compute_reservation_count(self):
        for record in self:
            record.reservation_count = self.env['hotel.reservation'].search_count([('guest_id', '=', record.id)])

    def action_view_reservations(self):
        return {
            'name': 'Guest Reservations',
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.reservation',
            'view_mode': 'list,form',
            'domain': [('guest_id', '=', self.id)],
            'context': {'default_guest_id': self.id},
        }


