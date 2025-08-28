# Punto 2
{
    'name': 'Inmobiliaria',
    'version': '1.0.0',
    'summary': 'Módulo de prueba para inmobiliaria',
    'category': 'Unla',
    'depends': ['base'],
    'data': [
        'security/real_estate_res_groups.xml', # Punto 12
        'security/ir.model.access.csv', # Punto 10
        'views/estate_property_views.xml', # Punto 5 y 17
        'views/real_estate_menuitem.xml' # Punto 6
    ],
    'installable': True,
    'application': True,
}
