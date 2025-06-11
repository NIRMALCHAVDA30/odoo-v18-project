{
    'name': 'Approval Workflow Task',
    'version': '18.0.1.0',
    'summary': 'This is Approval Workflow task odoo',
    'description': """    """,
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base','sale_management'],
    'data': [
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
