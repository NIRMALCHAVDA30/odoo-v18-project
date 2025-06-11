{
    'name': 'Learn Odoo',
    'version': '18.0.1.0',
    'summary': 'This is learning odoo',
    # 'sequence': 10,
    'description': """    """,
    # 'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['sale_management'],
    'data': [
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
