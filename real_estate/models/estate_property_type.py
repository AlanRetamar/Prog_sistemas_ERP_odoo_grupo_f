from odoo import models, fields

# ---- punto 25

# hereda de Model
class EstatePropertyType(models.Model): 
    _name = 'estate.property.type'
    _description = 'Tipos de propiedad'

    #campos
    name = fields.Char(string="Nombre", required=True)