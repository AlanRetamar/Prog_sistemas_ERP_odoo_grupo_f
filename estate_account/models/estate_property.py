from odoo import Command, models

#Punto 27 unidad 2
class EstateProperty(models.Model):
    _inherit= 'estate.property'
    
    def action_sold(self):
        for property in self:
            self.env["account.move"].create({
                "partner_id": property.buyer_id.id, # a. el partner_id deberá ser el comprador de la propiedad
                "move_type": "out_invoice", # b. el move_type deberá ser “out_invoice”, para indicar que es una factura a un cliente.
                "property_id": property.id,
                "line_ids": [
                   Command.create({            # c facturación con nombre, cantidad y precio unitario (campos técnicos “name”, “quantity” y “price_unit” respectivamente)
                       "name": property.name,  # La primera línea deberá tener el nombre de la propiedad, cantidad uno y precio de venta (selling_price) como precio unitario
                       "quantity": 1,
                       "price_unit": property.selling_price,
                   }),
                   Command.create({
                       "name": "Administrative Fees", # La segunda línea deberá ser “Gastos administrativos”, cantidad uno y cien como precio unitario.
                       "quantity": 1,
                       "price_unit": 100.00,
                   }) 
                ],
            })
        return super().action_sold() 