from odoo import api, models,fields
from odoo.exceptions import ValidationError
class ProductBundleQuantity(models.Model):
    _name = 'product.bundle.qty'

    is_add_range = fields.Boolean()
    qty_start = fields.Integer()
    qty_end = fields.Integer()
    discount_value = fields.Integer()
    bundle_id = fields.Many2one('product.bundle')

    @api.constrains('qty_start','qty_end')
    def check_qty_range(self):
        for rec in self:
            if rec.qty_end - rec.qty_start <=0 :
                raise ValidationError('Qty end must be larger than qty start')

