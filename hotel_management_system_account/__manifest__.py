{
    'name': 'Hotel Management System Account',
    'version': '18.0.1.0',
    'summary': '',
    # 'sequence': 10,
    'description': """    """,
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['hotel_management_system', 'account', 'sale_management'],
    'data': [
        "views/hotel_reservation_view.xml",
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
    ],  
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}