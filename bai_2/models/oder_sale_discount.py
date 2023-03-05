from odoo import api, fields, models

class SaleOrderDiscountWarranty(models.Model):
    _inherit = 'sale.order'

    sale_order_discount_warranty_estimated = fields.Float(string="Sale Order Discount Estimated By Warranty",compute="_compute_discount")
    def _compute_discount(self):
        for rec in self:
            if rec.product_template_id.product_warranty == 'VIP_10':
                rec.sale_order_discount_warranty_estimated = rec.amount_total/10
            elif rec.product_template_id.product_warranty == 'VIP_20':
                rec.sale_order_discount_warranty_estimated = rec.amount_total/5
            else:
                rec.sale_order_discount_warranty_estimated = 0