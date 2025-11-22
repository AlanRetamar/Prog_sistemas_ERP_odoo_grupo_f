from odoo import fields, models

#Punto 24 unidad 2
class ResUsers(models.Model):
    _inherit = "res.users"
    
    property_ids = fields.One2many(comodel_name="estate.property", inverse_name="salesman_id")