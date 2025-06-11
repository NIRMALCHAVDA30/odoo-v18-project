from odoo import api, models, fields
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError

class Estate(models.Model):
    _name = "estate.property"
    _description = "This is Real Estate Module"
    _order = "id desc"

    name = fields.Char(string="Name", required=True, default="Unknown")
    description = fields.Text(copy=False)
    postcode = fields.Char(size=8)
    available_from = fields.Date()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(default=False, string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Used for Orientation",
    )
    last_seen = fields.Datetime("Last seen", default=fields.Datetime.now)
    active = fields.Boolean(default=True)
    status = fields.Selection(
        [
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        default="new",
    )


    # Many2one 
    property_type_id = fields.Many2one(comodel_name="estate.property.type")
    buyer_id = fields.Many2one("res.partner", string="Buyer")   
    salesperson = fields.Many2one("res.users", string="Seller", default=lambda self: self.env.user)

    # Many2many
    tag_ids = fields.Many2many("estate.property.tag")

    # One2many
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="offer")

    #Computed Fields
    total = fields.Float(compute="_compute_total", string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total = record.living_area + record.garden_area



    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for i in self:
            i.best_price = max(i.offer_ids.mapped('price'), default=0.0)


    #onchange
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False


    # Action to apply in button
    def action_sold(self):
        print("=============+THIS IS INSIDE ACTION SOLD ESTATE")
        for record in self:
            if record.status == "cancelled":
                raise UserError("A cancelled property cannot be sold.")
            else:
                record.status = "sold"
        return {'name':'villa'}
    
    def action_cancel(self):
        for record in self:
            if record.status == "sold":
                raise UserError("A sold property cannot be cancelled.")
            else:
                record.status = "cancelled"
        return True
    
    #sql constrints
    _sql_constraints = [
    ("_check_expected_price_positive", "CHECK(expected_price >= 0)", "Expected price must be strictly positive"),
    ("_check_selling_price_positive", "CHECK(selling_price >= 0)", "Selling price must be positive"),
    ]


    # python constrains
    # @api.constrains("expected_price")
    # def _check_expected_price_positive(self):
    #     for record in self:
    #         if record.expected_price <= 0:
    #             raise ValidationError("Expected price must be strictly positive")
    
    # python constrains       
    @api.constrains("selling_price", "expected_price")
    def _check_selling_price(self):
        for record in self:
            if record.selling_price and record.selling_price < 0.9 * record.expected_price:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price")
            
    #postcode validation       
    @api.constrains("postcode")
    def _check_postcode(self):
        for record in self:
            if record.postcode:
                if not record.postcode.isdigit():
                    raise ValidationError("Postcode only digits.")
                if len(record.postcode) !=8:
                    raise ValidationError("Postcode only 8 digits.")
                
    
    #Python Inheritance
    #ondelete()
    def unlink(self):
        for record in self:
            if record.status in ['new', 'cancelled']:
                raise ValidationError("New or Cancelled property can not be deleted")
