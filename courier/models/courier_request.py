from odoo import models, fields, api,_

class CourierRequest(models.Model):
    _name = 'courier.request'
    _description = 'Courier Request'

    name = fields.Char(
        required=True, readonly=True, copy=False, default=lambda self: _("New")
    )

    #sequence
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", _("New")) == _("New"):
                vals["name"] = self.env["ir.sequence"].next_by_code("courier.request") or _("New")
            print("\n\n----------------------VALS_LIST-------------------", vals_list)
            print("\n\n..........................VALS.................", vals)

        return super().create(vals_list)

    #Sender 
    sender_name = fields.Char()

    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')

    sender_phone = fields.Char(string="Sender Phone Number")
    sender_email = fields.Char()

    #Receiver
    receiver_name = fields.Char()

    receiver_street = fields.Char()
    receiver_street2 = fields.Char()
    receiver_zip = fields.Char(change_default=True)
    receiver_city = fields.Char()
    receiver_state_id = fields.Many2one("res.country.state")
    receiver_country_id = fields.Many2one('res.country')

    receiver_phone = fields.Char(string="Receiver Phone Number")
    receiver_email = fields.Char()

    #Courier
    registration_date = fields.Date(default=fields.Date.today)
    delivery_date = fields.Date()

    type_id = fields.Many2one('courier.type')
    category_id = fields.Many2one('courier.categories')
    dimension_id = fields.Many2one('courier.dimension.price.rule', string="L ✘ W ✘ H")
    volumetric_weight_price = fields.Float(related='dimension_id.price')
    priority_id = fields.Many2one('courier.priorities')
    priority_amount = fields.Float(related='priority_id.charges')

    #internal
    tag = fields.Many2many('courier.tag')
    responsible_user = fields.Many2one("res.users", default=lambda self: self.env.user)

