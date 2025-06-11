{
    'name': 'Interview',
    'version': '18.0.1.0',
    'summary': 'Interview question',
    'description': """    """,
    'depends': ['base', 'sale_management'],
    'data': [
        "security/ir.model.access.csv",
        "views/sale_order_view.xml",
        "views/price_wizard_view.xml",
    ], 
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}