from datetime import timedelta
from odoo import models, fields, api 
from odoo.exceptions import UserError

# Punto 37
class EstatePropertyOffer(models.Model):
    _name= 'estate.property.offer'
    _description = 'Oferta sobre Propiedad'
    
    price = fields.Float(string="Precio", required=True)
    
    #Punto 9 unidad 2
    #9a
    validity = fields.Integer(string = "Validez (días)", default = 10 )
    #9b
    date_deadline = fields.Date(string="Fecha limite", compute="_compute_date_deadline",inverse="_inverse_date_deadline", store=True,)
    

    


    status = fields.Selection(
        selection=[
            ('accepted', 'Aceptada'),
            ('refused', 'Rechazada'),
        ]
    )
    
    partner_id = fields.Many2one(
        comodel_name = 'res.partner',
        string = 'Ofertante',
        required = True,
    )
    
    property_id = fields.Many2one(
        comodel_name = 'estate.property',
        string = 'Propiedad',
        required = True,
    )
    
    #Punto 11 unidad 2
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        string='Tipo de Propiedad',
        store=True,
        readonly=False,
        related_sudo=True
    )
    
    #Punto 18 unidad 2
    _sql_constraints = [('unique_offer_name','UNIQUE(partner_id, property_id)','Una persona solo puede hacer una oferta sobre una misma propiedad')]

    #Punto 10 unidad 2
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (record.create_date.date() +
                                        timedelta(days=record.validity))
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                # Calcula la diferencia en días entre date_deadline y create_date
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            elif record.date_deadline:
                # Si no hay create_date, usa la fecha actual
                delta = record.date_deadline - fields.Date.today()
                record.validity = delta.days
    #Punto 16 unidad 2            
    def action_accept_offer(self):
        """Acepta la oferta y actualiza la propiedad"""
        for record in self:
            # Verifica que la propiedad no esté vendida o cancelada
            if record.property_id.state in ['sold', 'canceled']:
                raise UserError('No se puede aceptar una oferta de una propiedad vendida o cancelada.')
            
            # a. Cargar el comprador y el precio de venta sobre la propiedad
            record.property_id.write({
                'buyer_id': record.partner_id.id,
                'selling_price': record.price,
                # b. Establecer en "oferta aceptada" el estado de la propiedad
                'state': 'offer_accepted',
            })
            
            # Marca esta oferta como aceptada
            record.status = 'accepted'
            
            # c. Establecer automáticamente en rechazada cada una de las demás ofertas
            other_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('id', '!=', record.id)
            ])
            other_offers.write({'status': 'refused'})
        
        return True
    
    #Punto 23 unidad 2 
    @api.model_create_multi
    def create(self, vals_list):
        offers = super().create(vals_list)  # Creamos las ofertas
        for offer in offers:
            property_id = offer.property_id

            # --- a) Precio debe ser mayor a la mejor oferta existente ---
            best_price = max(property_id.offer_ids.mapped('price') or [0])
            if offer.price < best_price:
                raise UserError("El valor de la nueva oferta debe ser mayor a la mejor oferta existente.")
            
             # --- b) Solo si el estado es 'new' u 'offer_received' ---
            if property_id.state not in ["new", "offer_received"]:
                raise UserError("Solo se pueden hacer ofertas sobre propiedades nuevas o con ofertas recibidas.")

            # --- c) Cambiar el estado de la propiedad ---
            property_id.state = "offer_received"

        return offers
        