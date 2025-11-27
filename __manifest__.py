{
    'name': 'Jasper CMS Content Manager',
    'version': '19.0.2.0.0',
    'category': 'Website',
    'summary': 'Manage website content sections, hero banners, and product grids',
    'description': """
        CMS Content Manager for Jasper - Luxury Stones & Crystals
        ==========================================================
        
        Features:
        - Meta tags management (SEO)
        - Hero sections with configurable layouts
        - Feature sections
        - Brand story sections
        - Product grid management
    """,
    'author': 'Alphaqueb Consulting',
    'website': 'https://alphaqueb.com',
    'license': 'LGPL-3',
    'depends': ['base', 'website', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/cms_meta_views.xml',
        'views/cms_section_views.xml',
        'views/cms_product_grid_views.xml',
        'views/cms_menus.xml',
        'data/cms_data.xml',
    ],
    'assets': {},
    'installable': True,
    'application': True,
    'auto_install': False,
}
