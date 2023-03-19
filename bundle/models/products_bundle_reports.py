from odoo import api,models,fields

class ProductsBundleSettings(models.Model):
    _name = 'products.bundle.settings'

    total_sale = fields.Float()
    total_save = fields.Float()