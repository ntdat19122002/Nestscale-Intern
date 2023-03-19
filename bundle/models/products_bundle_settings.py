from odoo import api,models,fields
class ProductBundleSettings(models.Model):
    _name = 'products.bundle.settings'

    bundle_position = fields.Selection([('below','Below add to cart form'),('above','Above add to cart form')])
    bundle_number =fields.Integer()
    bundle_title_color = fields.Char()
    button_lable = fields.Char()