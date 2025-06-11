{
    'name': 'Part 2',
    'version': '18.0.1.0',
    'summary': 'This is part 2 task odoo',
    'description': """    """,
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base','sale_management', 'hr_holidays', 'contacts', 'hr_timesheet'],
    'data': [
       "views/sale_order_template_view.xml",
       "views/ir_action_views.xml",
       "views/stock_picking_view.xml",
       "views/sale_order_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}