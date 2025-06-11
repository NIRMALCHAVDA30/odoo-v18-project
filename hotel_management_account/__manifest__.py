{
    'name': 'Hotel Management Account',
    'version': '18.0.1.0',
    'summary': '',
    # 'sequence': 10,
    'description': """    """,
    # 'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['hotel_management', 'account'],
    'data': [
        "views/xpath.xml",
    ],  
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}