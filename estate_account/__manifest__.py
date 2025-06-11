{
    'name': 'Estate Account',
    'version': '18.0.1.0',
    'summary': '',
    # 'sequence': 10,
    'description': """    """,
    # 'category': 'Accounting/Accounting',
    'website': 'https://www.odoo.com/app/invoicing',
    'depends': ['estate','account'],
    'data': [
        "report/estate_property_report.xml",
    ],  #'contacts'
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
