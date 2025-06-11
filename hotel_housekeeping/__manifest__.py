{
    'name': 'Hotel Housekeeping',
    'version': '18.0.1.0',
    'summary': 'This is the hotel housekeeping...',
    'description': """    """,
    'depends': ['base' ,'hotel_management_system','hr'],
    'data': [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/hotel_housekeeping_view.xml",
        "views/hotel_room_view.xml",
        "views/menus.xml",
    ], 
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}