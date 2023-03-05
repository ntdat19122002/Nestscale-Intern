import os

import jinja2

import odoo
from odoo.http import request
import json

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../static/html'))
loader = jinja2.FileSystemLoader(path)
jinja_env = jinja2.Environment(loader=loader, autoescape=True)
# jinja_env.filters["json"] = json.dumps
class BundleAPI(odoo.http.Controller):
    @odoo.http.route('/bundle', auth='public', type="http")
    def shop_bundle(self):
        template = jinja_env.get_template('app.html')
        products = request.env['product.product'].search([])
        res = template.render(products=products)
        return res