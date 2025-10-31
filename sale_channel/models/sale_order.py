from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    # Campo para seleccionar el Canal de Venta
    # Relacionado con el nuevo modelo sale.channel (Requisito 2a)
    channel_id = fields.Many2one(
        'sale.channel',
        string = 'Canal de venta',             
        required = True, # Obligatorio (Requisito 2a)
    )
    
    
    # Función que se ejecuta cada vez que cambia el campo 'channel_id'
    @api.onchange('channel_id')
    def _onchange_channel_id(self):
        """
        Modifica el almacén de la orden de venta (warehouse_id) al cambiar el canal.
        Esto asegura que las entregas subsiguientes usen el depósito asignado al canal.
        (Requisito 2b)
        """
        if self.channel_id and self.channel_id.warehouse_id:
            self.warehouse_id = self.channel_id.warehouse_id