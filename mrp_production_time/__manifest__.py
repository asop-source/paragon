{
    'name': 'MRP Production Time',
    'version': '17.0',
    'summary': 'Modul untuk manajemen waktu produksi MRP',
    'description': """
        Modul ini dirancang untuk mendukung manajemen waktu pada produksi MRP.
        Fitur-fitur meliputi pengaturan waktu produksi, penjadwalan, pemantauan proses produksi, dan pelaporan.
    """,
    'category': 'Manufacturing',
    'author': 'Asop',
    'website': 'https://www.yourcompanywebsite.com',
    'license': 'LGPL-3',
    'depends': [
        'mrp',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_production_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
