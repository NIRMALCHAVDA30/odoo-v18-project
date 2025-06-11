from odoo import models, fields, api,_
from odoo.exceptions import ValidationError

class CourierBooking(models.Model):
    _name = 'courier.booking'
    _inherit = ['mail.thread']
    _description = 'Courier Booking'

    name = fields.Char(
        required=True, readonly=True, copy=False, default=lambda self: _("New")
    )

    #sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("courier.booking") or _("New")
            print("\n\n----------------------VALS_LIST-------------------", vals_list)
            print("\n\n..........................VALS.................", vals)

        return super().create(vals_list)
    
    priority = fields.Selection([
        ("not_fav", "Not Fav"),
        ("fav", "Favourite")
    ])
    
    #Sender
    sender_id = fields.Many2one('res.partner', tracking=True, required=True)

    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(size=6)
    city = fields.Char(required=True)
    state_id = fields.Many2one("res.country.state", string="State")
    country_id = fields.Many2one('res.country', string="Country")

    sender_phone = fields.Char(string="Sender Phone Number", related='sender_id.phone')
    sender_email = fields.Char(related='sender_id.email', string="Sender Email")

    #Receiver
    receiver_id = fields.Many2one('res.partner', readonly=True)

    receiver_street = fields.Char()
    receiver_street2 = fields.Char()
    receiver_zip = fields.Char(size=6)
    receiver_city = fields.Char(required=True)
    receiver_state_id = fields.Many2one("res.country.state")
    receiver_country_id = fields.Many2one('res.country')

    receiver_phone = fields.Char(string="Receiver Phone Number", related='receiver_id.phone')
    receiver_email = fields.Char(related='receiver_id.email', string="Receiver Email")

    #Courier
    product_id = fields.Many2one('product.product', required=True)
    weight = fields.Float(required=True, string="Weight(Kg)")
    price_per_estimeted_cost = fields.Float()
    dimensions = fields.Char(required=True)
    delivery_priority = fields.Selection([
        ('cheapest', 'Cheapest'),
        ('balanced', 'Balanced'),
        ('fastest', 'Fastest'),
        ('all' , 'All')
    ], required=True)

    suggested_modes_ids = fields.One2many('shipping.suggestion', 'booking_id', string="Suggested Modes")
    selected_mode_id = fields.Many2one('shipping.mode', string="Selected Mode")
    route_id = fields.Many2one('shipping.route', string="Route")
    cost = fields.Monetary()
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)


    #Internal
    delivery_estimate = fields.Integer(string="Delivery Estimate(Days)")
    tracking_id = fields.Char(string="Tracking ID", readonly=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('invoiced', 'Invoiced'),
        ('picked', 'Picked'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out For Delivery'),
        ('delivered', 'Delivered'),
        ('returned', 'Returned')
    ], default='draft', tracking=True)
    agent_id = fields.Many2one('delivery.agent', string="Assigned Agent", readonly=True)
    pickup_time = fields.Datetime(readonly=True)
    delivery_time = fields.Datetime(readonly=True)
    delivery_proof = fields.Binary(readonly=True)
    
    complaint_ids = fields.One2many('customer.complaint', 'booking_id')

   

    #Generate Suggestion Button
    def action_generate_suggestions(self):
        print("\n\n\n\n\nbutton was clicked")
        for record in self:
           
            route = self.env['shipping.route'].search([
                    ('source_city', '=', record.city),
                    ('destination_city', '=', record.receiver_city)
                ], limit=1)
            print("\n\n\n\n\n---------ROUTE--->", route)

            record.route_id = route

            if record.delivery_priority == 'all':
                matching_lines = route.route_line_ids
            else:
                matching_lines = route.route_line_ids.filtered(
                    lambda rl: rl.mode_id.speed_rank == record.delivery_priority 
                )
            print("\n\n\n\n\n\n\n------------<<<MATCHING LINES>>>-------", matching_lines)
            print("\n\n---------RECORD->", record)
            
            suggestions = [(0, 0, {
                'booking_id': record.id, 
                'route_line_id': rl.id,
                'estimated_days': rl.estimated_days,
                'estimated_cost': rl.cost_per_kg,
                'suggestion_type': rl.mode_id.speed_rank if record.delivery_priority == 'all' else record.delivery_priority,
            }) for rl in matching_lines]
            print("\n\n>>>>SUGGESTIONS>>>>", suggestions)
            
            record.suggested_modes_ids = [(5,0,0)]
            record.suggested_modes_ids = suggestions

    #Confirm Button
    def action_confirm(self):
        self.status = "confirmed"

    #Invoice Button
    def action_create_invoice(self):  
        self.status = "invoiced"

    #state button invoice
    invoice_id = fields.Many2one("account.move", readonly=True)

    def action_view_invoice(self):
        return {
            "type": "ir.actions.act_window",
            "name": "Customer Invoice",
            "view_mode": "form",
            "res_model": "account.move",
            "res_id": self.invoice_id.id,
            "target": "current",
        }


    #Assign Delivery Agent button
    def action_open_assign_agent_wizard(self):
        for record in self:
            if record.agent_id:
                raise ValidationError("Delivery agent already assigned. You can not assign again.")
            if record.invoice_id.state != 'posted':
                raise ValidationError("You can only assign a delivery agent after the invoice is Paid.")
        return {
            'name': 'Assign Delivery Agent',
            'type': 'ir.actions.act_window',
            'res_model': 'assign.agent.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_booking_id': self.id
            }
        }
    

    # Complaints state button 
    complaint_count = fields.Integer(string="Complaint Count", compute="_compute_complaint_count")

    @api.depends('complaint_ids')
    def _compute_complaint_count(self):
        for record in self:
            record.complaint_count = len(record.complaint_ids)

    def action_view_complaints(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Complaints',
            'res_model': 'customer.complaint',
            'view_mode': 'list,form',
            'domain': [('booking_id', '=', self.id)],
            'target': 'current',
        }
    


    #Weight Validation
    @api.constrains('weight')
    def _check_weight_positive(self):
        for record in self:
            if record.weight <= 0:
                raise ValidationError("Weight must be greater than 0.")

   