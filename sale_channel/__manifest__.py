
{
    'name': 'Canal de Venta prueba cambio de  nombre',
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
        'views/sale_order_views.xml',
    ],
    'application': True,
}
