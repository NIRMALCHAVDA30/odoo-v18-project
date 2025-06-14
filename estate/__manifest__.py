{
    'name': 'Estate',
    'version': '18.0.1.0',
    'category' : 'Real Estate/Brokerage',
    'summary': 'This is Real Estate Module',
    # 'sequence': 10,
    'description': """    """,
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['contacts' , 'account' ,'account_payment'],
    'data': [
        "security/security.xml",
        "wizard/sold_property_wizard.xml",
        "security/ir.model.access.csv",
        "report/estate_property_templates.xml",
        "report/estate_property_reports.xml",
        "views/estate_property_views.xml",
        "views/estate_property_type_view.xml",
        "views/estate_property_tag_view.xml",
        "views/estate_property_offer_view.xml",
        "views/res_users_view.xml",
        "views/estate_menus.xml",
        "views/contact_website_view.xml",
        "views/estate_test_views.xml",
        # "data/master_data.xml",
    ],
    'demo': [
        "demo/demo_data.xml",
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
