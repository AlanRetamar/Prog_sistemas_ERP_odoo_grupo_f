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


    def _prepare_invoice(self):
        # 1. Llamar al método padre para obtener los valores base
        vals = super(SaleOrder, self)._prepare_invoice()
        
        # 2. Lógica para el Diario de Facturación (Punto 2.c) y Trazabilidad (Punto 2.d)
        if self.channel_id:
            # a. Asignar el Canal a la Factura (Parte del Punto 2.d)
            # Esto funciona porque ya agregaste 'channel_id' a account.move
            vals['channel_id'] = self.channel_id.id
            
            # b. Asignar el Diario de Facturación (Punto 2.c)
            # Usamos el campo correcto 'allowed_journal_id'
            if self.channel_id.allowed_journal_id:
                vals['journal_id'] = self.channel_id.allowed_journal_id.id
            else:
                # Opcional: Agregar una advertencia si falta el diario, 
                # o dejar que Odoo tome el diario por defecto si lo permite tu requerimiento.
                # Aquí simplemente deja que el flujo continúe con el diario que obtuvo del super()
                pass 
        return vals        
    def _prepare_picking_vals(self, group_id=False):
        """
        Sobrescribe para agregar el canal de venta al picking (Requisito 2.d).
        """
        # 1. Llamar al método padre para obtener los valores base
        vals = super(SaleOrder, self)._prepare_picking_vals(group_id)

        # 2. Asignar el Canal a la Orden de Entrega
        # (El related del paso 1 puede hacer esto, pero así nos aseguramos)
        if self.channel_id:
            vals['channel_id'] = self.channel_id.id
        return vals   
        