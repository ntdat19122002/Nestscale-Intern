from odoo import api,models,fields
class ProductBundle(models.Model):
    _inherit = 'product.product'

    qty = fields.Integer(default='1')
    discount_value = fields.Float()