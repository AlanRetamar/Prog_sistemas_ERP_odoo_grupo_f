# Punto 3
from odoo import models, fields
from datetime import date # Punto 20
from dateutil.relativedelta import relativedelta # Punto 20

class EstateProperty(models.Model):
    _name= 'estate.property'
    _description = 'Propiedades'

    name = fields.Char(string="Titulo", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Codigo Postal")
    # Punto 19 y 20
    date_availability = fields.Date(string="Fecha disponibilidad", copy=False, default=lambda self: date.today() + relativedelta(months=3)) 
    expected_price = fields.Float(string="Precio esperado")
    selling_price = fields.Float(string="Precio de venta", copy=False) # Punto 19
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Superficie cubierta")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Jardin")
    garden_orientation = fields.Selection(
        selection=[
            ('north', 'Norte'),
            ('south', 'Sur'),
            ('east', 'Este'),
            ('west', 'Oeste'),
        ],
        default="north",
        string="Orientación del jardín"
    )
    garden_area = fields.Integer(string="Superficie jardín")
    
    # Punto 21
    state = fields.Selection(
        selection=[
            ('new', 'Nuevo'),
            ('offer_received', 'Oferta recibida'),
            ('offer_accepted', 'Oferta aceptada'),
            ('sold', 'Vendido'),
            ('canceled', 'Cancelado'),
        ],
        default="new",
        string="Estado",
        required=True,
        copy=False
    )
    
    # Punto 29 a
    property_type_id = fields.Many2one(
        comodel_name = 'estate.property.type',
        string = 'Tipo Propiedad',
    )
    
    # Punto 29 b
    buyer_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Comprador',
    )
    
    # Punto 29 c
    salesman_id = fields.Many2one(
        comodel_name = 'res.users',
        string = 'Vendedor',
        copy=False,
        default=lambda self: self.env.user,
    )
    
    # Punto 35
    tag_ids = fields.Many2many(
        comodel_name = 'estate.property.tag',
        string = 'Etiquetas',
    )
    
    # Punto 39
    offer_ids = fields.One2many(
        comodel_name = "estate.property.offer",
        inverse_name = "property_id",
        string = "Ofertas",
    )


