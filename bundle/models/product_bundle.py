from odoo import api,models,fields
class ProductBundle(models.Model):
    _inherit = 'product.product'

    qty = fields.Integer()
    discount_value = fields.Float()