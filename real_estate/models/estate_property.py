# Punto 3
from odoo import models, fields, api, Command
from datetime import date # Punto 20
from dateutil.relativedelta import relativedelta # Punto 20
from odoo.exceptions import UserError
import random


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
    # offer_ids trae todas las ofertas relacionadas con la propiedad.
    offer_ids = fields.One2many(
        comodel_name = "estate.property.offer",
        inverse_name = "property_id",
        string = "Ofertas",
    )
    
    #Punto 19 unidad 2
    # Agregar en estate.property un campo offer_partner_ids que contenga todas las personas (res.partner) que hicieron ofertas 
    # sobre esa propiedad.
    offer_partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string='Personas que ofertaron',
        compute='_compute_offer_partner_ids',
    )
    
    #.mapped('partner_id') obtiene todos los ofertantes (res.partner) de esas ofertas.
    @api.depends('offer_ids.partner_id')
    def _compute_offer_partner_ids(self):
        for record in self:
            record.offer_partner_ids = record.offer_ids.mapped('partner_id')


    
    #Punto 13 unidad 2
    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area = 10 if self.garden else 0

    #Punto 1 unidad 2
    total_area = fields.Integer(string="Superficie total", compute="_compute_total_area", store = True) #Punto 4 unidad 2
    
    #Punto 7 unidad 2
    best_offer = fields.Float(string='Mejor oferta', compute='_compute_best_offer')
    
    
    @api.depends("garden_area","living_area") #Punto 5 unidad 2
    def _compute_total_area(self): #Punto 1 unidad 2
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area
            
    #Punto 7 unidad 2   
    def _compute_best_offer(self):
        for rec in self:
            offers = rec.offer_ids.mapped('price')
            rec.best_offer = max(offers) if offers else 0

    #Punto 14 unidad 2
    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        if self.expected_price and self.expected_price < 10000:
            return {
                'warning': {
                    'title': 'Advertencia',
                    'message': 'El precio esperado es menor a $10,000'
                }
            }
            
    #Punto 15 unidad 2
    def action_sold(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Una propiedad cancelada no puede ser marcada como vendida.')
            record.state = 'sold'
        return True
    
    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Una propiedad vendida no puede ser cancelada.')
            record.state = 'canceled'
        return True   
    
    #Punto 20 unidad 2
    def action_generate_offer(self):
        for record in self:
            if not record.expected_price:
                raise UserError("Debe establecer un precio esperado antes de generar una oferta automática.")
            
            # a Calcular precio aleatorio entre -30% y +30%
            variation = random.uniform(-0.3, 0.3)
            offer_price = record.expected_price * (1 + variation)

            # b Buscar contactos activos que aún no ofertaron
            eligible_partners = self.env['res.partner'].search([
                ('active', '=', True),
                ('id', 'not in', record.offer_partner_ids.ids)
            ])

            if not eligible_partners:
                raise UserError("No hay contactos disponibles que no hayan ofertado sobre esta propiedad.")
            
            # b Elegir uno al azar
            selected_partner = random.choice(eligible_partners)

            # Crear la oferta
            self.env['estate.property.offer'].create({
                'price': offer_price,
                'partner_id': selected_partner.id,
                'property_id': record.id,
            })
            
        return True
    
    #Punto 21 unidad 2
    def action_clear_tags(self):   
        self.tag_ids = [Command.clear()]   # a) Limpia todas las etiquetas
    
        return True
    
    def action_load_all_tags(self):
        all_tags = self.env['estate.property.tag'].search([]).mapped('id')
        self.tag_ids = [Command.set(all_tags)]  # b) Cargar todas las etiquetas existentes

        return True
    
    def action_add_new_tag(self):
        tag_model = self.env['estate.property.tag']
        # Busca si existe la etiqueta A estrenar
        new_tag = tag_model.search([('name', '=', 'A estrenar')], limit=1)
        
        if not new_tag:
            # Crear etiqueta si no existe
            new_tag = tag_model.create({'name': 'A estrenar'})
        
        self.tag_ids = [Command.link(new_tag.id)]  # c) Vincula sin borrar las existentes
        return True
    
    #Punto 22 unidad 2
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_canceled(self):
        if any(p.state not in ["new", "canceled"] for p in self):
            raise UserError("Las propiedades solo van a ser borradas cuando su estado es 'Nuevo' o 'Cancelado'")
  
    

        