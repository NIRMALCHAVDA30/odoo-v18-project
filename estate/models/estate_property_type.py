from odoo import api, models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is Estate Property Type Module"
    _order = "name"

    name = fields.Char("Name",required=True)
    # property_type = fields.Selection([("house" , "House"),
                                    #   ("vila" , "Vila"),
                                    #   ("flat" , "Flat"),
                                    #   ("pg", "Pg"),
                                    #   ("farm" , "Farm")])       

    _sql_constraints = [("_unique_property_type", "UNIQUE(name)", "Type name must be unique")]


    property_ids = fields.One2many("estate.property" , "property_type_id" , string="Properties")

    sequence = fields.Integer()


    ##
    offer_count = fields.Integer(string="Offers", compute="_compute_offer_count")

    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")


    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
            print(">>>>>>>>>>>>....", record.offer_count)

    # button is clicked when perform thr action
    def action_view_offers(self):
        return {
            "name": "Offers",
            "type": "ir.actions.act_window",
            "res_model": "estate.property.offer",
            "view_mode": "list,form",
            "domain": [("property_type_id", "in", self.ids)],  # Handles multiple records
            "context": {"default_property_type_id": self.id},
        }

        