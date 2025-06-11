from odoo import api, models, fields
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is Estate Property Offer Module"
    _order = "price desc"

    name = fields.Char("Name")
    price = fields.Integer()
    partner_id = fields.Many2one("res.partner", required=True)
    status = fields.Selection([("refused", "Refused"), 
                               ("accepted", "Accepted")], default=None, copy=False)

    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7, store=True)
    date_deadline = fields.Date(string="Deadline",compute="_compute_date_deadline",inverse="_inverse_date_deadline", store=True)

    # @api.depends("create_date", "validity")
    # def _compute_date_deadline(self):
    #     for record in self:
    #         print(record)
    #         base_date = record.create_date.date() if record.create_date else fields.Date.today()
    #         record.date_deadline = fields.Date.add(base_date , days=record.validity)

    # def _inverse_date_deadline(self):
    #     for record in self:
    #         base_date = record.create_date.date() if record.create_date else fields.Date.today()
    #         record.validity = (record.date_deadline - base_date).days

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            print(record.create_date)
            if record.create_date and record.validity:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            print("----------------",record.date_deadline)
            print("**************", record.create_date.date())
            if record.date_deadline and record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
    
    #action 
    def action_accept(self):
        for record in self:
            if record.property_id:
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
                record.property_id.status = "sold"
            record.status = "accepted" 
            
            
    def action_refuse(self):
        for record in self:
            record.status = "refused"

    #sql constraints
    _sql_constraints = [("_check_price_positive" , "CHECK(price>0)", "Offer price must be strictly positive")]

    # @api.constrains("price")
    # def _check_selling_price_positive(self):
    #     for record in self:
    #         if record.price < 0:
    #             raise ValidationError("Offer price must be strictly positive")

    ##  Related fields.
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id", store=True)

    #python inheritance
    @api.model
    def create(self, vals):
        print("***************SELF*>",self)
        print("\n\n\n---------------VALS->", vals)
        if vals.get("property_id") and vals.get("price"):
            property = self.env["estate.property"].browse(vals["property_id"])

            if property.offer_ids:
                max_offer = max(property.mapped("offer_ids.price"))
                if vals["price"] < max_offer:
                    raise UserError("The offer must be higher than %.2f"  % max_offer)  
                property.status = "offer received"
            return super().create(vals)
        

