{
    'name': 'Product Bundle',
    'version': '1.0.0',
    'category': 'Sale',
    'author': 'Odoo Mates',
    'sequence':-99,
    'summary': 'Product management system',
    'description': """Product management system""",
    'depends': ['sale'],
    'data':[
        'security/ir.model.access.csv',
        'views/product_bundle_view.xml',
        'views/app.xml'
    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}