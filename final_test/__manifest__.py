{
    'name': 'Final Test',
    'version': '18.0.1.0',
    'summary': 'This is final test odoo',
    'description': """    """,
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base', 'hr', 'hr_holidays','account','sale_management'],
    'data': [
       "views/hr_leave_view.xml",
       "views/account_move_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}