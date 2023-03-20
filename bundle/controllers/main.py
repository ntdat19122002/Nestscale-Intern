import math
import os
import jinja2

import odoo
from odoo.http import request, Response
import json

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../static/html'))
loader = jinja2.FileSystemLoader(path)
jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps
class BundleAPI(odoo.http.Controller):
    @odoo.http.route('/bundle', auth='public', type="http", cors="*")
    def shop_bundle(self):
        template = jinja_env.get_template('index.html')
        res = template.render()
        return res

    @odoo.http.route('/bundle/api/page/<int:page>', auth='public', type="http", cors="*")
    def shop_page_bundle_api(self, page):
        page_number = page
        per_page = 20

        offset = 0 if page_number <= 1 else (page_number - 1) * per_page
        records = request.env['product.template'].sudo().search_read(
            [],order='description_sale', offset=offset, limit=per_page
        )

        response = []
        for record in records:
            image = ''
            if isinstance(record['image_1024'], bytes):
                image = record['image_1024'].decode('utf-8')
            response.append({"id": record['id'], "name": record['name'], "image":image, 'price': record['lst_price']})

        result = {
            'status': 'success',
            'products': response,
            'page_number': page_number if page_number > 0 else 1,  # current page number
            'per_page': per_page,  # records per page
            'max_page': math.ceil(request.env['product.template'].sudo().search_count([])/per_page)
        }
        return Response(json.dumps(result), mimetype='application/json')

    # Get product with id
    @odoo.http.route('/bundle/api/product/<int:id>', auth='public', type="http", cors="*")
    def product_bundle_api(self,id):
        templates = request.env['product.template'].sudo().browse(id)
        products = templates.product_variant_ids
        data = {}
        products_data = []
        for product in products:
            # tier
            request.env.cr.execute("SELECT product_bundle_id "
                                   "FROM tier_products "
                                   "WHERE product_product_id = %s" % product.id)
            bundle_tier_ids = (x[0] for x in request.env.cr.fetchall())
            bundle_tiers = request.env['product.bundle'].sudo().browse(bundle_tier_ids)
            bundle_tier_data = []
            for bundle_tier in bundle_tiers:
                if self.checkBundle(bundle_tier):
                    bundle_qty_data = []
                    for bundle_qty in bundle_tier.bundle_qty:
                        bundle_qty_data.append({
                            'start':bundle_qty.qty_start,
                            'end':bundle_qty.qty_end,
                            'discount_value':bundle_qty.discount_value,
                            'highlight_enable':bundle_qty.highlight_enable
                        })
                    bundle_tier_data.append({
                        'title': bundle_tier.title,
                        'discount_type': bundle_tier.discount_type,
                        'qty' : bundle_qty_data
                    })

            # total
            request.env.cr.execute("SELECT product_bundle_id "
                                   "FROM total_products "
                                   "WHERE product_product_id = %s" % product.id)
            bundle_total_ids = (x[0] for x in request.env.cr.fetchall())
            bundle_totals = request.env['product.bundle'].sudo().browse(bundle_total_ids)
            bundle_total_data = []
            for bundle_total in bundle_totals:
                if self.checkBundle(bundle_total):
                    products_bundle = []
                    for product_bundle in bundle_total.total_products:
                        price_after = self.priceAfter(product_bundle.lst_price,bundle_total.discount_type,bundle_total.discount_value)
                        if isinstance(product_bundle.image_1024, bytes):
                            image = product_bundle.image_1024.decode('utf-8')
                        products_bundle.append({
                            'name' : product_bundle.name,
                            'price': product_bundle.lst_price,
                            'price_after': price_after,
                            'image': image,
                        })
                    bundle_total_data.append({
                        'title': bundle_total.title,
                        'products': products_bundle,
                        'total': bundle_total.total_origin_price(),
                        'sale_total': bundle_total.price_total_bundle(),
                        'discount_type':bundle_total.discount_type
                    })

            # each
            request.env.cr.execute("SELECT product_bundle_id "
                                   "FROM each_products "
                                   "WHERE product_product_id = %s" % product.id)
            bundle_each_ids = (x[0] for x in request.env.cr.fetchall())
            bundle_eachs = request.env['product.bundle'].sudo().browse(bundle_each_ids)
            bundle_each_data = []
            for bundle_each in bundle_eachs:
                if self.checkBundle(bundle_each):
                    products_bundle = []
                    for product_bundle in bundle_each.each_products:
                        price_after = self.priceAfter(product_bundle.lst_price,bundle_each.discount_type,product_bundle.discount_value)
                        if isinstance(product_bundle.image_1024, bytes):
                            image = product_bundle.image_1024.decode('utf-8')
                        products_bundle.append({
                            'name': product_bundle.name,
                            'price': product_bundle.lst_price,
                            'price_after': price_after,
                            'image': image,
                        })
                    bundle_each_data.append({
                        'title': bundle_each.title,
                        'products': products_bundle,
                        'total':bundle_each.total_origin_price(),
                        'sale_total':bundle_each.price_each_bundle()
                    })

            if isinstance(product.image_1024, bytes):
                image = product.image_1024.decode('utf-8')
            products_data.append({
                'id'   : product.id,
                'name' : product.name,
                'price': product.lst_price,
                'image': image,
                'bundle_tier' : bundle_tier_data,
                'bundle_total': bundle_total_data,
                'bundle_each' : bundle_each_data
            })
        data['products'] = products_data
        return json.dumps(data)

    # check bundle validation
    def checkBundle(self,bundle):
        if bundle.enable == False:
            return False
        return True

    # caculate price after sale
    def priceAfter(self,price,type,value):
        if type == 'percentage':
            price_after = price*(1-value/100)
        if type == 'hard_fix':
            price_after = price-value
        if type == 'total_fix':
            price_after = value
        return round(price_after,2)

    @odoo.http.route('/add-to-cart', auth='public', type="json", cors="*", methods=['POST'])
    def addToCart(self,**kwargs):
        id = kwargs.get('id')
        quantity = kwargs.get('quantity')

        request.env['cart.line'].sudo().create({
            'product':id,
            'quantity': quantity
        })