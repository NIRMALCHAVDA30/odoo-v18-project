from odoo import models, fields, api
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    #Task 14
    def action_post(self):
        return super().action_post()
    
    def action_post(self):
        for record in self:
            print("\n\n\n----------->", record)
            if record.move_type == 'in_invoice':
                threshold = record.company_id.vendor_bill_threshold
                print("\n\n\n---------->",record.company_id)
                print("\n\n\n THRESOLD==========>", threshold)
                
                if record.amount_total > threshold:
                    if not self.env.user.has_group('account.group_account_manager'):
                        raise UserError(
                            "You cannot validate this vendor bill because the threshold of %.2f set."  % threshold)
        return super().action_post()
    

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

