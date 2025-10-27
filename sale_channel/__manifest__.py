
{
    'name': 'Canal de Venta',
    'author': 'UNLa',
    'version': '1.0.0',
    'description': 'Módulo de Canal de Venta',
    'depends': [
        'base',
        'sale_management',
        'account',
        'stock',
    ],
    'data': [
        'security/sale_channel_res_groups.xml',
        'security/ir.model.access.csv',
        'views/sale_channel_views.xml',
        'views/sale_channel_menuitem.xml',
    ],
    'application': True,
}
