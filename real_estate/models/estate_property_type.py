from odoo import models, fields
# ---- punto 25

# hereda de Model
class EstatePropertyType(models.Model): 
    _name = 'estate.property.type'
    _description = 'Tipos de propiedad'

    #Punto 17 unidad 2
    _sql_constraints = [('unique_type_name','UNIQUE(name)','El nombre del tipo de propiedad debe ser único')]
    
    #campos
    name = fields.Char(string="Nombre", required=True)