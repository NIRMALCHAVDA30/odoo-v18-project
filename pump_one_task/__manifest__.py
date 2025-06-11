{
    'name': 'Pump One Task',
    'version': '18.0.1.0',
    'summary': 'This is Pump one task odoo',
    'description': """    """,
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base','sale_management', 'contacts'],
    'data': [
        "views/res_partner_view.xml",
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
