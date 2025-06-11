from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    #Task 4: Get  User who has the access right of Inventory admin
    def get_inventory_admin_users(self):
        inventory_admin_group = self.env.ref('stock.group_stock_manager')
        
       
        users = self.env['res.users'].search([
            ('groups_id', 'in', inventory_admin_group.id)
        ])

       
        print("\n\n\n******************> Users with Inventory Admin Rights:")
        for user in users:
            print(f"User: {user.name}")

        return True

    #Task :Find all users with access to both inventory and accounting modules
    def find_user_with_access_to_both_inventory_and_accounting(self):
        inventory_admin_group = self.env.ref('stock.group_stock_manager')
        account_admin_group = self.env.ref("account.group_account_manager")

        users = self.env['res.users'].search([
            ('groups_id', 'in', [inventory_admin_group.id,account_admin_group.id])
        ])
    
        print("\n\n\n******************> Users with Inventory Admin Rights & account_admin_group right:")
        for user in users:
            print(f"User: {user.name}\n\n\n")

    
