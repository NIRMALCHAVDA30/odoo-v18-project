{
    'name': 'Hotel Maintenance',
    'version': '18.0.1.0',
    'summary': 'This is the hotel maintenance...',
    'description': """    """,
    'depends': ['base' ,'hotel_management_system', 'hr'],
    'data': [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/hotel_maintenance_view.xml",
    ], 
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}