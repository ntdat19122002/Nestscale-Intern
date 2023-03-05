from odoo import api,models,fields
from odoo.exceptions import ValidationError

class Bundle(models.Model):
    _name = 'product.bundle'

    title = fields.Char(required=True)
    description = fields.Char()
    type = fields.Selection([('bundle','Multiple Product Bundle (Discount by Purchasing Multiple Products)'),
                             ('tier','Quantity Break Bundle (Discount by Purchasing a Product in a Larger Quantity)')],required=True)
    discount_rule = fields.Selection([('discount_total','Discount on Total Bundle'),('discount_products','Discount on Each Products/variants')],required=True)
    discount_type = fields.Selection([('percentage','Percentage'),('hard_fix','Hard Fix'),('total_fix','Total Fix')],required=True)
    discount_value = fields.Float()
    enable = fields.Boolean(string="Enable Bundle")
    active = fields.Boolean(default=True)
    priority = fields.Integer()
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    indefinite_bundle = fields.Boolean()

    total_products = fields.Many2many('product.product','total_products')
    each_products = fields.Many2many('product.product','each_products')
    tier_products = fields.Many2many('product.product','tier_products')
    @api.onchange('indefinite_bundle')
    def change_indefinite_bundle(self):
        for rec in self:
            if rec.indefinite_bundle:
                rec.start_time = False
                rec.end_time = False

    @api.constrains('discount_value')
    def check_discount_value(self):
        for rec in self:
            if rec.discount_value <= 0:
                raise ValidationError('Discount value must be positive')

    @api.constrains('title')
    def check_title(self):
        a = self.env['product.bundle'].search([])
        for rec in self:
            for reca in a[:-1]:
                if rec.title == reca.title:
                    raise ValidationError('Title must be unique')

