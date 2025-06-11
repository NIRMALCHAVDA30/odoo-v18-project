{
    'name': 'CRC Sales Task',
    'version': '18.0.1.0',
    'summary': 'This is CRC Sales task odoo',
    'description': """    """,
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['base','sale_management'],
    'data': [
        "security/ir.model.access.csv",
        "data/scheduled_action.xml",
        "views/subscription_plan_view.xml",
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
