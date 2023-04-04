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
            bundle_tiers = request.env['product.bundle'].sudo().browse(product.get_bundle_tier_ids())
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
                        'id' : bundle_tier.id,
                        'title': bundle_tier.title,
                        'discount_type': bundle_tier.discount_type,
                        'qty' : bundle_qty_data
                    })

            # total

            bundle_totals = request.env['product.bundle'].sudo().browse(product.get_bundle_total_ids())
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
                        'id': bundle_total.id,
                        'title': bundle_total.title,
                        'products': products_bundle,
                        'total': bundle_total.total_origin_price(),
                        'sale_total': bundle_total.price_total_bundle(),
                        'discount_type':bundle_total.discount_type
                    })

            # each

            bundle_eachs = request.env['product.bundle'].sudo().browse(product.get_bundle_each_ids())
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
                        'id':bundle_each.id,
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

    @odoo.http.route('/cart', auth='public', type='http', cors='*')
    def Cart(self):
        cart_lines = request.env['cart.line'].sudo().search([])
        bundles = request.env['product.bundle'].sudo().search([],order='priority ,type')
        data={}
        cart_line_data = []
        product_lst = {}
        total = 0
        for cart_line in cart_lines:
            if isinstance(cart_line.product.image_1024, bytes):
                image = cart_line.product.image_1024.decode('utf-8')
            total += cart_line.product.lst_price*cart_line.quantity
            cart_line_data.append({
                'id':cart_line.id,
                'product':{
                    'id': cart_line.product.id,
                    'name':cart_line.product.name,
                    'image':image,
                    'price':cart_line.product.lst_price,
                },
                'quantity':cart_line.quantity
            })
            product_lst[cart_line.product.id]=cart_line.quantity

        lst = {}
        self.get_bundle_data_ids(lst,product_lst,bundles)
        print(lst)

        bundles_data = []
        discount_total = 0
        for key,value in lst.items():
            bundle_discount = request.env['product.bundle'].browse(key)
            if  bundle_discount.type == 'bundle':
                if bundle_discount.discount_rule == 'discount_total':
                    discount = bundle_discount.total_origin_price() - bundle_discount.price_total_bundle()
                else:
                    discount = bundle_discount.total_origin_price() - bundle_discount.price_each_bundle()
                bundles_data.append({
                    'title':bundle_discount.title,
                    'discount': discount,
                    'quantity':value
                })
                discount_total+=discount*value

        data['cart_lines']=cart_line_data
        data['bundles'] = bundles_data
        data['discount_total'] = discount_total
        data['total']=total
        return json.dumps(data)

    def get_bundle_data_ids(self,lst,product_lst,bundles):
        print(bundles)
        print(product_lst)
        tmp = lst.copy()
        print(tmp)
        for bundle in bundles:
            check = True
            for products in bundle.total_products:
                for product in products:
                    print(product.id)
                    if product.id not in product_lst:
                        check = False
            for products in bundle.each_products:
                for product in products:
                    print(product.id)
                    if product.id not in product_lst:
                        check = False
            for products in bundle.tier_products:
                check = False
                # for product in products:
                #     print(product.id)
                #     if product.id not in product_lst:
                #         check = False
            print(check)
            if check:
                if bundle.id not in lst:
                    lst[bundle.id] = 0
                lst[bundle.id] += 1
                for product in bundle.total_products:
                    product_lst[product.id] -= 1
                    if product_lst[product.id] == 0:
                        del product_lst[product.id]
                for product in bundle.each_products:
                    product_lst[product.id] -= 1
                    if product_lst[product.id] == 0:
                        del product_lst[product.id]
        if tmp == lst:
            return lst
        else:
            return self.get_bundle_data_ids(lst, product_lst, bundles)

    @odoo.http.route('/add-to-cart', auth='public', type="json", cors="*", methods=['POST'])
    def addToCart(self,**kwargs):
        id = kwargs.get('id')
        quantity = kwargs.get('quantity')

        cart_line = request.env['cart.line'].sudo().search([('product','=',id)])

        if not cart_line:
            request.env['cart.line'].sudo().create({
                'product':id,
                'quantity': quantity
            })
        else:
            cart_line.write({'quantity': (cart_line.quantity + quantity)})

    @odoo.http.route('/add-bundle-to-cart/<int:id>', auth='public', type="http", cors="*")
    def addBundleToCart(self, id):
        bundle = request.env['product.bundle'].sudo().browse(id)
        if bundle.discount_rule == 'discount_total':
            for product in bundle.total_products:
                cart_line = request.env['cart.line'].sudo().search([('product','=',product.id)])
                if not cart_line:
                    request.env['cart.line'].sudo().create({
                        'product': product.id,
                        'quantity': 1
                    })
                else:
                    cart_line.write({'quantity': (cart_line.quantity + 1)})
        if bundle.discount_rule == 'discount_products':
            for product in bundle.each_products:
                cart_line = request.env['cart.line'].sudo().search([('product','=',product.id)])
                if not cart_line:
                    request.env['cart.line'].sudo().create({
                        'product': product.id,
                        'quantity': 1
                    })
                else:
                    cart_line.write({'quantity': (cart_line.quantity + 1)})
    @odoo.http.route('/update-cart-line/<int:id>/quantity/<int:quantity>', auth='public', type="http", cors="*")
    def updateCartLine(self,id,quantity):
        request.env['cart.line'].sudo().browse(id).write({'quantity': quantity})

    @odoo.http.route('/delete-cart-line/<int:id>', auth='public', type="http", cors="*")
    def deleteCartLine(self,id):
        request.env['cart.line'].sudo().browse(id).unlink()

    @odoo.http.route('/length-cart', auth='public', type="http", cors="*")
    def lenCart(self):
        length = 0
        for cart_line in request.env['cart.line'].sudo().search([]):
            length += cart_line.quantity
        return json.dumps({'length':length})