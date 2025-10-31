# Punto 1
from odoo import models, fields
from datetime import date
from odoo.exceptions import ValidationError
import random


class SaleChannel(models.Model):
    _name= 'sale.channel'
    _description = 'Canal de Venta'


    name = fields.Char(string="Name", required=True)
    code = fields.Char(string="Code", required=True)

    warehouse_id = fields.Many2one(
        comodel_name = 'stock.warehouse',
        string = 'Warehouse',
    )

    allowed_journal_id = fields.Many2one(
        'account.journal',
        string="Allowed Journals",
    )

    _sql_constraints = [
        ('codigo_unique', 'unique(code)', 'El código del canal ya existe en el sistema.')
    ]

  
    

        