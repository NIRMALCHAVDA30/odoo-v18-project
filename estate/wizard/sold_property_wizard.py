from odoo import fields, models

class SoldPropertyWizard(models.TransientModel):
    _name = "sold.property.wizard"
    _description = "Sold Property Wizard"

    startdate = fields.Date(required=True)
    enddate = fields.Date(required=True)
    
    def action_button_generate(self):
        print("\n\n\nGenerate button was clicked...\n\n\n")

    def action_button_cancel(self):
        print("\n\n\nCancel butoon was clicked...\n\n\n")



