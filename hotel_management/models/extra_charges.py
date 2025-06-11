from odoo import api, models, fields

class ExtraCharges(models.Model):
    _name = "extra.charges"
    _description = "Extra Charges"

    name = fields.Char(string="Charge Name", required=True)
    charge_type = fields.Selection([
        ('per_person', 'Per Person'),
        ('fixed', 'Fixed Amount')
    ], string="Charge Type", required=True, default="per_person")

    amount = fields.Float(required=True)
    description = fields.Text()

    quantity = fields.Integer(default=1, required=True)
    total_cost = fields.Float(compute="_compute_total_cost", store=True)
    
    @api.depends("quantity", "amount")
    def _compute_total_cost(self):
        for record in self:
            record.total_cost = record.quantity * record.amount