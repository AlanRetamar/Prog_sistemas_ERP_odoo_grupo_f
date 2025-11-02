from odoo import models, fields

class StockPicking(models.Model):
    _inherit = "stock.picking" # Heredamos la Orden de Entrega

   
    channel_id = fields.Many2one(
        'sale.channel',
        string='Canal de Venta',
        readonly=True,
        store=True,
        related='sale_id.channel_id', 
    )