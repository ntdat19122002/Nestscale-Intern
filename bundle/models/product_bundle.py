from odoo import api,models,fields
class ProductBundle(models.Model):
    _inherit = 'product.product'

    qty = fields.Integer(default='1')
    discount_value = fields.Float()

    def get_bundle_tier_ids(self):
        self.env.cr.execute("SELECT product_bundle_id "
                               "FROM tier_products "
                               "WHERE product_product_id = %s" % self.id)
        bundle_tier_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_tier_ids

    def get_bundle_total_ids(self):
        self.env.cr.execute("SELECT product_bundle_id "
                               "FROM total_products "
                               "WHERE product_product_id = %s" % self.id)
        bundle_total_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_total_ids

    def get_bundle_each_ids(self):
        self.env.cr.execute("SELECT product_bundle_id "
                               "FROM each_products "
                               "WHERE product_product_id = %s" % self.id)
        bundle_each_ids = (x[0] for x in self.env.cr.fetchall())
        return bundle_each_ids