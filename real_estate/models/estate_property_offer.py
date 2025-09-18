from odoo import models, fields
# Punto 37
class EstatePropertyOffer(models.Model):
    _name= 'estate.property.offer'
    _description = 'Oferta sobre Propiedad'
    
    price = fields.Float(string="Precio", required=True)
    
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
    
