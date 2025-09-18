from odoo import models, fields

# ---- punto 31

# hereda de Model
class EstatePropertyTag(models.Model): 
    _name = 'estate.property.tag'
    _description = 'Etiqueta de propiedad'

    #campos
    name = fields.Char(string="Nombre", required=True)