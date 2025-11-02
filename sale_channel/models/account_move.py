from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"
    channel_id = fields.Many2one(
        'sale.channel',
        string='Canal de Venta',
        readonly=True, # Lo ponemos de solo lectura porque solo es para trazabilidad
        store=True, # Asegura que se guarde en la base de datos
    )
