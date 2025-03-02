# C:\Users\heric\odoo-dev-projects\addons\real_estate_ads\__manifest__.py
{
    "name": "Real Estate Ads",
    "version": "1.0",
    "website": "https://www.yourcompany.com", 
    "author": "Heric Libong",
    "description": """
        Real Estate module to show available properties for sale or rent.
    """,
    "category": "Sales",
    "depends": ["base"],
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/menu_items.xml',

        # Data files
        #'data/property_type.xml',
        'data/estate.property.type.csv',
        'data/property_tag.xml'
        
        
    ],
    "demo": [
        #'demo/property_tag.xml',
    ],
    "installable": True,
    "application": True,
    "license": "LGPL-3",
}