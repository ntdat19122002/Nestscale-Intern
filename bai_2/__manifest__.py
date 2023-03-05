{
    'name': 'Product Warranty',
    'version': '1.0.0',
    'category': 'Sale',
    'author': 'Odoo Mates',
    'sequence':-99,
    'summary': 'Warranty management system',
    'description': """Warranty management system""",
    'depends': ['sale'],
    'data':[
        'security/security.xml',
        'views/warranty_sale.xml',
        'views/guarantor_view.xml',
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}