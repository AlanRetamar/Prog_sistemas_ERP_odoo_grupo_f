# Punto 2
{
    'name': 'Inmobiliaria',
    'author': 'UNLa',
    'version': '1.0.0',
    'description': 'Módulo de prueba para inmobiliaria',
    'depends': [
        'base'
    ],
    'data': [
        'security/real_estate_res_groups.xml', # Punto 12
        'security/ir.model.access.csv', # Punto 10
        'views/estate_property_views.xml', # Punto 5 y 17
        'views/estate_property_type_views.xml', # Punto 27
        'views/estate_property_tag_views.xml', # Punto 27
        'views/estate_property_offer_views.xml', # Punto 40
        'views/real_estate_menuitem.xml', # Punto 6
    ],
    'application': True,
}
