{
    'name': 'Hotel Restaurant',
    'version': '18.0.1.0',
    'summary': 'This is the hotel restaurant...',
    'description': """    """,
    'depends': ['base' ,'hotel_management_system', 'lunch'],
    'data': [
        "security/ir.model.access.csv",
        "views/hotel_restaurant_view.xml",
        "views/restaurant_order_view.xml",
        "views/hotel_guest_view.xml",
        "views/hotel_menus.xml",
    ], 
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}