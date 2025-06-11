from odoo import api, models, fields


class ResPartner(models.Model):
    _inherit = "res.partner"
    _rec_names_search = ['name', 'email', 'phone']

    # Task 12
    # @api.model
    # def name_search(self, name="", args=None, operator="ilike", limit=100):
    #     args = list(args or [])
    #     if not name:

    #         return super().name_search(
    #             name=name, args=args, operator=operator, limit=limit
    #         )

    #     domain = ["|","|",
    #         ("name", operator, name),
    #         ("email", operator, name),
    #         ("phone", operator, name),
    #     ]

    #     if args:
    #         domain = ["&"] + args + domain
    #         print("\n\n\n+++++++++++++++", domain)

    #     partners = self.search_fetch(domain, ["display_name"], limit=limit)
    #     return [(partner.id, partner.display_name) for partner in partners]
    

    #Task 13
    @api.depends('name', 'phone')
    def _compute_display_name(self):
        for record in self:
            if record.phone:
                record.display_name = f"{record.name} - {record.phone}"
            else:
                record.display_name = record.name