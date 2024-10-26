{
    'name': 'Product Data Sync to Z',
    'version': '1.0.0',
    'category': 'Inventory',
    'summary': 'Synchronize product data from Odoo to external application Z*',
    'description': """
            This module captures changes to product master data in Odoo and synchronizes it with an external application Z*. 
            It triggers synchronization on create, update, and delete actions of product records.
            """,
    'author': 'Asop',
    'website': 'https://yourwebsite.com',
    'depends': ['base', 'product'],  # Pastikan modul base dan product ada
    'data': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
