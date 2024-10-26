# __manifest__.py
{
    'name': 'Inventory Product Rule',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Manage allowed products for specific locations',
    'description': """
        This module allows users to define rules for products that are allowed to be transferred to specific locations.
        It adds a menu for managing location product rules and enforces these rules during stock transfers.
    """,
    'depends': ['base','stock'],
    'data': [
        'security/group_user.xml',  # Menambahkan file keamanan
        'views/location_product_rules_views.xml',
    ],
    'installable': True,
    'application': False,
}
