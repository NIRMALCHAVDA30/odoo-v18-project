from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = "stock.picking"

    # Task 8
    terms_conditions = fields.Html(string="Terms and Conditions")


    #Task 9
    country_of_origin = fields.Many2one('res.country',string="Country of Origin",compute="_compute_country_of_origin",store=True)


    @api.depends('partner_id')
    def _compute_country_of_origin(self):
        for record in self:
            record.country_of_origin = record.partner_id.country_id

    is_invisible = fields.Boolean(compute="_compute_country", store=True)

    @api.depends('partner_id')
    def _compute_country(self):
        for record in self:
            record.is_invisible = record.partner_id.country_id != record.company_id.partner_id.country_id