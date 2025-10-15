from odoo import fields, models

#Punto 27 unidad 2
class AccountMove(models.Model):
    _inherit = "account.move"
    
    property_id = fields.Many2one(comodel_name = "estate.property")