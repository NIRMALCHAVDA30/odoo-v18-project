from odoo import models, api, fields, Command# type: ignore
from odoo.exceptions import UserError # type: ignore
from datetime import date, timedelta , datetime
import random

class CourierBooking(models.Model):
    _name = 'courier.booking'
    _rec_name = 'booking_sequence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "booking_sequence"
  
    is_favorite = fields.Boolean()
    booking_sequence = fields.Char(string="Courier Sequence")
    sender_id = fields.Many2one("res.partner","Sender Name",required=True)
    street = fields.Char(related='sender_id.street',readonly=False, string="Reciver's Street",required=True)
    city = fields.Char(related='sender_id.city',readonly=False ,string="Pickup City",required=True)
    state_id = fields.Many2one("res.country.state",related='sender_id.state_id' , string='State',required=True, domain="[('country_id.code', '=', 'IN')]",readonly=False,  help='Select a state from India only')
    country_id = fields.Many2one("res.country",related='sender_id.country_id',readonly=False)
    phone = fields.Char(string="Sender's Phone", required=True)
    zip = fields.Char()
    
    internal_notes = fields.Html()
    reciever_id = fields.Many2one("res.partner", "Reciver Name")
    reciever_street = fields.Char(readonly=False, related='reciever_id.street', string="Reciver's Street")
    reciever_city = fields.Char(readonly=False, string="Destination City",required=True)
    reciever_state_id = fields.Many2one("res.country.state" ,required=True, string='State', domain="[('country_id.code', '=', 'IN')]",readonly=False,  help='Select a state from India only')
    reciever_country_id = fields.Many2one("res.country",related='reciever_id.country_id',readonly=False)
    reciever_phone = fields.Char(readonly=False, string="Reciver's Phone",required=True)
    reciever_zip = fields.Char(related='reciever_id.zip',readonly=False)
    tag_ids = fields.Many2many("courier.tags")
    per_kg_cost = fields.Float()
    product_id = fields.Many2one("product.product",required=True)
    color=fields.Integer()
    courier_date = fields.Date(default=date.today())
    is_flag= fields.Boolean(default="False")
    width = fields.Char("Width")
    height = fields.Char("Height")
    weight = fields.Char("Weight")
    length = fields.Char("Length")
    delivery_priority = fields.Selection(
        selection = [('cheapest','Low'),('balanced','Medium'),('fastest','High'),('all','See All')],default="cheapest"
    )
    suggested_modes_ids = fields.One2many("shipping.suggestion","booking_id")
    selected_mode_id = fields.Many2one("shipping.mode")
    route_id = fields.Many2one("shipping.route",readonly=True)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                 default=lambda self: self.env.user.company_id.currency_id)
    tracking_id = fields.Char()
    cost = fields.Monetary(currency_field='currency_id',string="Cost")
    delivery_estimate = fields.Integer()
    state = fields.Selection(
        selection = [('draft','Draft'),('confirmed','Confirmed'),('invoiced','Invoiced'),('picked','Picked'),
                     ('in_transit','In Transit'),('out_for_delivery','Out For Delivery'),('delivered','Delivered')
                     ],default="draft", tracking=True
        )
    rating = fields.Selection(
        selection=[('1', 'low'), ('2', 'medium'),
                   ('3', 'good'), ('4', 'very good'),
                   ('5', 'excellent'),('6','brilliant')],
        string="Rating",
        default='5',help="Give Ratings To Delivery Agent."
    )
    is_chosen = fields.Boolean(string="Is Chosen",default=False,store=True)
    agent_id = fields.Many2one("delivery.agent")
    pickup_time = fields.Datetime()
    in_transit_time = fields.Datetime()
    out_for_delivery_time = fields.Datetime()
    delivered_time = fields.Datetime()
    delivery_proof = fields.Image()
    complaint_ids = fields.One2many("customer.complaint","booking_id", tracking=True)
    invoice_ids = fields.One2many("account.move","booking_id")
    payment_detail = fields.Selection([
        ('paid', 'Paid'), ('unpaid', 'Unpaid')],store=True, compute = "_compute_payment_check")
    invoice_id = fields.Many2one("account.move")
    agent_phone = fields.Char()
    delivery_notes = fields.Text()
    @api.onchange('delivery_priority')
    def _onchange_(self):
        self.is_chosen = False
    
    
    @api.constrains('zip','reciever_zip')
    def _check_zip(self):
        for rec in self:
            if rec.zip:
                if not rec.zip.isdigit():
                    raise UserError("Zip  must contain only digits.")
                if len(rec.zip) != 6:
                    raise UserError("Zip  must be exactly 6 digits long.")
    
    @api.constrains('phone','reciever_phone')
    def _check_phone(self):
        for rec in self:
            if rec.phone:
                if not rec.phone.isdigit():
                    raise UserError("Phone number must contain only digits.")
                if len(rec.phone) != 10 and len(rec.phone) > 0:
                    print(len(rec.phone))
                    raise UserError("Phone number must be exactly 10 digits long.")
    
    @api.constrains('weight')
    def _check_weight(self):
        for rec in self:
            if rec.weight:
                if not rec.weight.isdigit():
                    raise UserError("Weight number must contain only digits.")
               
    def action_invoice_generate(self):
        for rec in self:
            if rec.invoice_ids:
                raise UserError('Your Invoice is Already Generated, Pay Now to Go Further.')
            if not rec.weight or not rec.per_kg_cost or not rec.product_id:
                raise UserError("Weight, Per kg cost, and Product must be provided to generate invoice.")
            try:
                weight = float(rec.weight)
            except ValueError:
                raise UserError("Weight must be a number.")
            journal = self.env["account.journal"].search([('type', '=', 'sale')], limit=1) 
            invoice = self.env["account.move"].create({
                'journal_id': journal.id,
                'move_type': 'out_invoice',
                'partner_id': rec.sender_id.id,
                'invoice_line_ids': [
                    Command.create({
                        'name': rec.product_id.name,
                        'product_id': rec.product_id.id,
                        'quantity': weight,
                        'price_unit': rec.per_kg_cost,
                        'currency_id': rec.currency_id.id,
                    }),
                ],
            })
            rec.invoice_ids += invoice
            print(rec.invoice_ids)
            invoice.action_post()
                
    @api.onchange('agent_id')
    def _onchange_agent_phone(self):
        for rec in self:
                rec.agent_phone = rec.agent_id.agent_phone
                
    @api.depends('invoice_ids.payment_state', 'invoice_ids')
    def _compute_payment_check(self):
        for rec in self:
            if rec.invoice_ids and all(invoice.payment_state == 'paid' for invoice in rec.invoice_ids):
                rec.payment_detail = 'paid'
                rec.state = 'invoiced'
            else:
                rec.payment_detail = 'unpaid'

    def action_assign_delivery(self):
        return {
            'name': 'Assign Delivery Agent',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.agent',
            'target': 'new',
            'view_mode': 'form',
            'context': {
                'default_booking_id':self.id
                        }
        }
    def action_assign_delivery_check(self):
        pass

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals['booking_sequence'] = self.env['ir.sequence'].next_by_code('booking.sequence')
        return super().create(vals_list)
     
    def action_view_invoice(self):
        self.ensure_one()         
        if self.invoice_ids:
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.move",
                "view_mode": "form",
                "res_id": self.invoice_ids[0].id,
                "target": "current",
            }
            print(self.invoice_ids[0].id,"----->Invoice Ids")
        else:
            raise UserError("No Invoice found for this Courier.")

    def action_view_complaints(self):
        self.ensure_one()
        if self.complaint_ids:
             return {
                "type": "ir.actions.act_window",
                "res_model": "customer.complaint",
                "view_mode": "list,form",
                "res_id": self.complaint_ids[0].id,
                "target": "current",
            }
        else:
            raise UserError("No Complaints Found For This Courier.")

    def action_suggestions(self):
        for booking in self:
            if not booking.city or not booking.reciever_city:
                raise UserError("Please Fill Source City and Destination City.")
            
            if booking.suggested_modes_ids:
                booking.suggested_modes_ids.unlink()
            matching_routes = self.env['shipping.route'].search([
                ('source_city', '=', booking.city),
                ('destination_city', '=', booking.reciever_city)
            ])
            priority = booking.delivery_priority
            booking.is_chosen = False
            for route in matching_routes:
                booking.route_id = route.id
                if priority == 'all':
                    filtered_lines = route.route_line_ids.filtered(
                        lambda line: line.is_active and line.mode_id
                    )
                else:
                  filtered_lines = route.route_line_ids.filtered(
                        lambda line: line.is_active and line.mode_id and
                        line.mode_id.speed_rank == priority
                    )
                for line in filtered_lines:
                    suggestion_type = (
                        line.mode_id.speed_rank if priority == 'all'
                        else priority
                    )
                    if suggestion_type not in ['cheapest', 'balanced', 'fastest']:
                        continue  
                    self.env['shipping.suggestion'].create({
                        'booking_id': booking.id,
                        'route_line_id': line.id,
                        'estimated_days': line.estimated_days,
                        'estimated_cost': line.cost_per_kg,
                        'currency_id': booking.currency_id.id,
                        'suggestion_type': suggestion_type
                    })
                    
    def action_confirmed_state(self):
        for rec in self:
            rec.state = 'confirmed'
            print("State is confirmed")
    