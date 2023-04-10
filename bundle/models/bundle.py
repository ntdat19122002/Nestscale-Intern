from odoo import api,models,fields
from odoo.exceptions import ValidationError

class Bundle(models.Model):
    _name = 'product.bundle'

    title = fields.Char(required=True)
    description = fields.Char()
    type = fields.Selection([('bundle','Multiple Product Bundle (Discount by Purchasing Multiple Products)'),
                             ('tier','Quantity Break Bundle (Discount by Purchasing a Product in a Larger Quantity)')],required=True,default='bundle')
    discount_rule = fields.Selection([('discount_total','Discount on Total Bundle'),('discount_products','Discount on Each Products/variants')],required=True,default='discount_total')
    discount_type = fields.Selection([('percentage','Percentage'),('hard_fix','Hard Fix'),('total_fix','Total Fix')],required=True,default='percentage')
    discount_value = fields.Float()
    enable = fields.Boolean(string="Enable Bundle", default=True)
    active = fields.Boolean(default=True)
    priority = fields.Integer()
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    indefinite_bundle = fields.Boolean()

    total_products = fields.Many2many('product.product','total_products')
    each_products = fields.Many2many('product.product','each_products')
    tier_products = fields.Many2many('product.product','tier_products')
    bundle_qty = fields.One2many('product.bundle.qty','bundle_id')

    def total_origin_price(self):
        total_price = 0
        if self.type == 'bundle' and self.discount_rule == 'discount_total':
            for product in self.total_products:
                total_price += product.lst_price
        elif self.type == 'bundle' and self.discount_rule == 'discount_products':
            for product in self.each_products:
                total_price += product.lst_price
        return total_price

    def price_total_bundle(self):
        if self.discount_type == 'percentage':
            price_bundle = self.total_origin_price()*(1-self.discount_value/100)
        elif self.discount_type == 'hard_fix':
            price_bundle = self.total_origin_price() - self.discount_value
        elif self.discount_type == 'total_fix':
            price_bundle = self.discount_value
        return round(price_bundle,2)

    def price_each_bundle(self):
        price_bundle = 0
        if self.discount_type == 'percentage':
            for product in self.each_products:
                price_bundle += product.lst_price*(1-product.discount_value/100)
        elif self.discount_type == 'hard_fix':
            for product in self.each_products:
                price_bundle += product.lst_price - product.discount_value
        elif self.discount_type == 'total_fix':
            for product in self.each_products:
                price_bundle += product.discount_value
        return round(price_bundle, 2)

    def price_tier_bundle(self,product,num,discount_value):
        price_bundle = 0
        if self.discount_type == 'percentage':
            price_bundle = product.lst_price * (1 - discount_value / 100) * num
        elif self.discount_type == 'hard_fix':
            price_bundle = (product.lst_price - discount_value) * num
        elif self.discount_type == 'total_fix':
            price_bundle = discount_value
        return round(price_bundle, 2)

    @api.onchange('indefinite_bundle')
    def change_indefinite_bundle(self):
        for rec in self:
            if rec.indefinite_bundle:
                rec.start_time = False
                rec.end_time = False

    @api.constrains('discount_value')
    def check_discount_value(self):
        for rec in self:
            if rec.type == 'bundle' and rec.discount_rule == 'discount_total':
                if rec.discount_value <= 0:
                    raise ValidationError('Discount value must be positive')

    @api.constrains('title')
    def check_title(self):
        a = self.env['product.bundle'].search([])
        for rec in self:
            for reca in a[:-1]:
                if rec.title == reca.title:
                    raise ValidationError('Title must be unique')

