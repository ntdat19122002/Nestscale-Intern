from odoo import api, fields, models

class SaleOrderDiscount(models.Model):
    _inherit = 'sale.order'

    sale_order_discount_estimated = fields.Float(string="Sale Order Discount Estimated",compute="_compute_discount")

    def _compute_discount(self):
        for rec in self:
            if rec.partner_id.customer_discount_code == 'VIP_10':
                rec.sale_order_discount_estimated = rec.amount_total/10
            elif rec.partner_id.customer_discount_code == 'VIP_20':
                rec.sale_order_discount_estimated = rec.amount_total/5
            else:
                rec.sale_order_discount_estimated = 0