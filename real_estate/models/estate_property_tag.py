from odoo import models, fields
# ---- punto 31

# hereda de Model
class EstatePropertyTag(models.Model): 
    _name = 'estate.property.tag'
    _description = 'Etiqueta de propiedad'
    
    #Punto 17 unidad 2
    _sql_constraints = [('unique_tag_name','UNIQUE(name)','El nombre de la etiqueta debe ser único')]

    #campos
    name = fields.Char(string="Nombre", required=True)