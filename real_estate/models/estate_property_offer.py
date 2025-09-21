from odoo import models, fields

# ---- punto 37

# hereda de Model
class EstatePropertOffer(models.Model): 
    _name = 'estate.property.offer'
    _description = 'Oferta sobre propiedad'

    #campos
    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(string="Estado", selection=[
                                                    ("accepted", "Aceptada"),
                                                    ("refused", "Rechazada")
                                                ])
    partner_id = fields.Many2one(comodel_name= "res.partner", string="Ofertante", required=True)
    property_id = fields.Many2one(comodel_name= "estate.property", string="Propiedad", required=True)