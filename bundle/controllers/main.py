import os
import jinja2

import odoo
from odoo.http import request
import json

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../static/html'))
loader = jinja2.FileSystemLoader(path)
jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps
class BundleAPI(odoo.http.Controller):
    @odoo.http.route('/bundle', auth='public', type="http")
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

    # Get product with id
    @odoo.http.route('/bundle/api/<int:id>', auth='public', type="http", cors="*")
    def product_bundle_api(self,id):
        product = request.env['product.product'].browse(id)
        image = ''
        if isinstance(product.image_1024, bytes):
            image = product.image_1024.decode('utf-8')
        products_data = {
            'id': product.id,
            'name': product.name,
            'price': product.lst_price,
            'image': image
        }
        return json.dumps(products_data)
