from odoo import api,models,fields
import re

class Customer(models.Model):
    _inherit = 'res.partner'

    customer_discount_code = fields.Text(string="Customer Discount Code")
    check_code = fields.Boolean(compute='_compute_check_code', store=True)

    @api.depends('customer_discount_code')
    def _compute_check_code(self):
        for rec in self:
            if re.search("VIP_[0-9]+",rec.customer_discount_code):
                rec.check_code = True
            else:
                rec.check_code = False

