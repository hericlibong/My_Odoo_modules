{
    'name': 'Odoo DAM Module',
    'version': '1.0',
    'summary': 'Digital Asset Management module for Odoo',
    'description': """
        This module provides Digital Asset Management (DAM) capabilities within Odoo.
        It allows users to manage, organize, and retrieve digital assets efficiently.
    """,
    'author': 'Heric Libong',
    'website': 'https://github.com/hericlibong/odoo-dam-module/wiki',
    'category': 'Tools',
    'depends': ['base', 'project'],
    'data': [
        'security/resource_groups.xml',
        'security/ir.model.access.csv',
        'views/resource_views.xml',
        'views/resource_menu.xml',
        'views/resource_log_view.xml',
    ],
    'demo': [
        # List your demo files here
    ],
    'installable': True,
    'application': True,
    "license": "LGPL-3",
}