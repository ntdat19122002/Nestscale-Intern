from odoo import api,models,fields
class Cart(models.Model):
    _name = 'cart.line'

    product = fields.Many2one('product.product')
    quantity = fields.Integer()
