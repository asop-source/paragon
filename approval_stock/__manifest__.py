# -*- coding: utf-8 -*-
{
    'name': "Approval Stock",

    'summary': """
            Approval Stock
        """,

    'description': """
        Approval Stock
    """,

    'author': "Asop",

    'category': 'stock',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','account'],

    # always loaded
    'data': [
        # 'security/groups.xml',
        'security/ir.model.access.csv',
        'views/stock_location.xml',
        'views/stock_picking.xml',
        'views/stock_quant.xml',
        'wizard/rejected_back_wizard.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        
    ],
}