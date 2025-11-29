{
    'name': 'The Brand CMS API',
    'version': '1.0',
    'category': 'Website/CMS',
    'summary': 'Gestor de contenido headless para The Brand Page',
    'description': """
        Módulo diseñado para gestionar el contenido de la página 'The Brand'.
        - API Pública HTTP (REST-like)
        - Gestión de Historias/Capítulos
        - Soporte directo para subida de Imágenes
        - Estructura visual basada en pestañas
    """,
    'author': 'Alphaque Consulting',
    'website': 'https://alphaque.com',
    'depends': ['base'], 
    'data': [
        'security/ir.model.access.csv',
        'data/cms_data.xml',   # <--- MOVIDO ANTES DE LAS VISTAS
        'views/cms_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}