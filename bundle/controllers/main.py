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

    # Get all products
    @odoo.http.route('/bundle/api', auth='public', type="http", cors="*")
    def shop_bundle_api(self):
        products = request.env['product.product'].search([])
        data = {}
        products_data = []
        for product in products:
            image = ''
            if isinstance(product.image_1024, bytes):
                image = product.image_1024.decode('utf-8')
            products_data.append(
                {
                    'id':product.id,
                    'name':product.name,
                    'price':product.lst_price,
                    'image':image
                }
            )
        data['products'] = products_data
        return json.dumps(data)

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
            request.env.cr.execute("SELECT product_bundle_id "
                                   "FROM tier_products "
                                   "WHERE product_product_id = %s" % product.id)
            bundle_tier_ids = (x[0] for x in request.env.cr.fetchall())
            bundle_tiers = request.env['product.bundle'].sudo().browse(bundle_tier_ids)
            bundle_tier_data = []
            for bundle_tier in bundle_tiers:
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


            request.env.cr.execute("SELECT product_bundle_id "
                                   "FROM total_products "
                                   "WHERE product_product_id = %s" % product.id)
            bundle_total_ids = (x[0] for x in request.env.cr.fetchall())
            bundle_totals = request.env['product.bundle'].sudo().browse(bundle_total_ids)
            bundle_total_data = []
            for bundle_total in bundle_totals:
                products_bundle = []
                for product_bundle in bundle_total.total_products:
                    if isinstance(product_bundle.image_1024, bytes):
                        image = product_bundle.image_1024.decode('utf-8')
                    products_bundle.append({
                        'name' : product_bundle.name,
                        'price': product_bundle.lst_price,
                        'image': image,
                    })
                bundle_total_data.append({
                    'title': bundle_total.title,
                    'products': products_bundle
                })

            request.env.cr.execute("SELECT product_bundle_id "
                                   "FROM each_products "
                                   "WHERE product_product_id = %s" % product.id)
            bundle_each_ids = (x[0] for x in request.env.cr.fetchall())
            bundle_eachs = request.env['product.bundle'].sudo().browse(bundle_each_ids)
            bundle_each_data = []
            for bundle_each in bundle_eachs:
                products_bundle = []
                for product_bundle in bundle_each.each_products:
                    if isinstance(product_bundle.image_1024, bytes):
                        image = product_bundle.image_1024.decode('utf-8')
                    products_bundle.append({
                        'name': product_bundle.name,
                        'price': product_bundle.lst_price,
                        'image': image,
                    })
                bundle_each_data.append({
                    'title': bundle_each.title,
                    'products': products_bundle
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

    # Get template with id
    @odoo.http.route('/bundle/api/template/<int:id>', auth='public', type="http", cors="*")
    def template_bundle_api(self,id):
        product = request.env['product.template'].sudo().browse(id)
        image = ''
        if isinstance(product.image_1024, bytes):
            image = product.image_1024.decode('utf-8')
        products_data = {
            'id': product.id,
            'name': product.name,
            'price': product.lst_price,
            'image': image,
            'description':product.description_sale
        }
        return json.dumps(products_data)
