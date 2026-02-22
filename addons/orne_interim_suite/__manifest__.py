{ 
    'name': 'Orne Interim Suite', 
    'version': '1.0', 
    'summary': 'Gestion des missions d\'intérim pour agences locales', 
    'description': '''Module de gestion des demandes de mission pour agences d\'intérim spécialisées BTP et Nettoyage.''', 
    'author': 'AC', 
    'website': 'https://github.com/hericlibong/My_Odoo_modules', 
    'category': 'Human Resources', 
    'depends': ['base'],  # Dépendances minimales pour le MVP
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/mission_views.xml',
        'views/menus.xml',
    ],  # Accès + séquence + vues + menus
    'demo': [],  # Pas de données demo pour cette phase
    'installable': True, 
    'application': True, 
    'auto_install': False, 
    'license': 'LGPL-3',
}