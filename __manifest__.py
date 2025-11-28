{
    'name': 'HOME Content Manager',
    'version': '19.0.3.0.0',
    'category': 'Website',
    'summary': 'Manage Home Page content and SEO',
    'description': """
        HOME Content Manager
        ====================
        
        Simplified manager specifically for the Home Page.
        - SEO Settings
        - Hero Section
        - Feature Section
        - Brand Story Section
    """,
    'author': 'Alphaqueb Consulting',
    'website': 'https://alphaqueb.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/home_views.xml',
        'views/menus.xml',
        'data/home_data.xml',
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
}