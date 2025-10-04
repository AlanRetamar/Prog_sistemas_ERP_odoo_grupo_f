from datetime import timedelta
from odoo import models, fields, api 


# Punto 37
class EstatePropertyOffer(models.Model):
    _name= 'estate.property.offer'
    _description = 'Oferta sobre Propiedad'
    
    price = fields.Float(string="Precio", required=True)
    validity = fields.Integer(string = "Validez (días)", default = 10 )
   
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
    property_type_id = fields.Many2one(
        related='property_id.property_type_id',
        string='Tipo de Propiedad',
        store=True
    )

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