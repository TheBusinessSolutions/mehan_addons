# -*- coding: utf-8 -*-

import json
import string
from werkzeug.exceptions import NotFound

from odoo.osv import expression
from odoo.http import request
from odoo import fields, http, _
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale

# Alan Shop Page Customization
class AtharvaWebsiteSaleExtend(WebsiteSale):

    def _get_search_domain(self, search, category, attrib_values, search_in_description=True):
        res = super(AtharvaWebsiteSaleExtend, self)._get_search_domain(search, category, attrib_values, search_in_description)
        res = expression.OR([res, [('product_brand_id', 'in', [int(b) for b in request.httprequest.args.getlist('brand',)])],\
                [('product_rating', 'in', [int(r) for r in request.httprequest.args.getlist('rating')])],\
                [('product_tags_ids', 'in', [int(t) for t in request.httprequest.args.getlist('tag')])]])
        return res

    @http.route([])
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, ppg=False, **post):

        rating_list = request.httprequest.args.getlist('rating')
        brand_list = request.httprequest.args.getlist('brand')
        tag_list = request.httprequest.args.getlist('tag')
        request.website = request.website.with_context(brands=brand_list,rating=rating_list,tags=tag_list)
        res = super(AtharvaWebsiteSaleExtend, self).shop(page, category, search, min_price, max_price, ppg, **post)
        ProductAttribute = request.env['product.attribute']
        productBrands = request.env['as.product.brand']
        productTags = request.env['product.tags']
        productCat = request.env['product.public.category']
        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attributes_ids = {v[0] for v in attrib_values}
        products = res.qcontext.get("products",[])
        pricelist_context, pricelist = self._get_pricelist_context()
        website_domain = request.website.website_domain()
        filter_by_price_enabled = request.website.is_view_active('website_sale.filter_products_price')
        if filter_by_price_enabled:
            company_currency = request.website.company_id.currency_id
            conversion_rate = request.env['res.currency']._get_conversion_rate(company_currency, pricelist.currency_id, request.website.company_id, fields.Date.today())
        else:
            conversion_rate = 1

        options = {
            'displayDescription': True,
            'displayDetail': True,
            'displayExtraDetail': True,
            'displayExtraLink': True,
            'displayImage': True,
            'allowFuzzy': not post.get('noFuzzy'),
            'min_price': float(min_price) / conversion_rate,
            'max_price': float(max_price) / conversion_rate,
            'attrib_values': attrib_values,
            'display_currency': pricelist.currency_id,
        }

        if category:
            if type(category) == str:
                options.update({'category':category})
            else:
                options.update({'category':str(category.id)})

        product_count, details, fuzzy_search_term = request.website._search_with_fuzzy("products_only", search,
            limit=None, order=self._get_search_order(post), options=options)
        search_product = details[0].get('results', request.env['product.template']).with_context(bin_size=True)
        if products:
            attributes = ProductAttribute.search([('product_tmpl_ids', 'in', search_product.ids),('visibility', '=', 'visible')])
        else:
            attributes = ProductAttribute.browse(attributes_ids)
        variant_count = self._variant_count(search_product, attributes)
        common_domain = [('active','=',True), ('website_id', 'in', (False, request.website.id))]
        brand_ids = productBrands.search(common_domain)
        tag_ids = productTags.search(common_domain)
        rating_count, brand_count, tag_count = self._rbt_count(search_product, brand_ids, tag_ids)
        category_count = self._category_count(website_domain, productCat, search_product)
        keep = QueryURL('/shop', category=category and int(category),
                        search=search,
                        attrib=attrib_list,
                        min_price=min_price, max_price=max_price,
                        order=post.get('order'),
                        rating=rating_list,
                        brand=brand_list,
                        tag=tag_list)

        category_tags = False
        Category = request.env['product.public.category']
        if category:
            if type(category) == str:
                category_tags = Category.search([('parent_id', '=', category)] + website_domain)
            else:
                category_tags = Category.search([('parent_id', '=', category.id)] + website_domain)

        res.qcontext.update({
            'keep':keep,
            'attributes_ids':attributes_ids,
            'variant_count':variant_count,
            'category_tags':category_tags,
            'brand_count':brand_count,
            'modal_cat_list': [cat.id for cat in productCat.search([] + website_domain)],
            "modal_brand_list":[brand.id for brand in brand_ids],
            'category_count':category_count,
            'tag_count':tag_count,
            'sel_tag_list':tag_list,
            'alphabets': list(string.ascii_uppercase),
            'all_tag_list':tag_ids,
            'sel_brand_list':brand_list,
            'all_brand_list':brand_ids,
            'rating_count':rating_count,
            'rating':rating_list,
            'as_shop':True
        })
        return res

    def _variant_count(self, search_product, attributes):
        ''' Default attribute counter'''
        attr_count = {}
        attrs_line = request.env['product.template.attribute.line'].search([('product_tmpl_id','in',search_product.ids)])
        for attr in attributes:
            for val in attr.value_ids:
                attr_count[str(val.id)] = 0
        if attrs_line:
            for each_line in attrs_line:
                for val in each_line.value_ids:
                    if str(val.id) in attr_count:
                        attr_count[str(val.id)] += 1
        return attr_count

    def _rbt_count(self, search_product, brand_list, tag_list):
        ''' Rating Brand Tag(rbt)counter'''
        brand_count = { str(brand.id) : 0 for brand in brand_list }
        tag_count = { str(tag.id) : 0 for tag in tag_list }
        rating_count = { rating : 0 for rating in range(1,5) }
        for prod in search_product:
            if prod.product_brand_id and prod.product_brand_id in brand_list:
                brand_count[str(prod.product_brand_id.id)] += 1
            if prod.product_tags_ids:
                for tag in prod.product_tags_ids:
                    if str(tag.id) in tag_count:
                        tag_count[str(tag.id)] += 1
            for rat in range(1,5):
                if prod.product_rating >= rat:
                    rating_count[rat] += 1
        return rating_count, brand_count, tag_count

    def _category_count(self,website_domain, productCatg, productTemplate):
        '''Category counter base on product'''
        categories = productCatg.search(website_domain)
        category_count = { str(cat.id):0 for cat in categories }
        Product = request.env['product.template'].with_context(bin_size=True)
        for cat in categories:
            search_product = Product.search_count([('public_categ_ids', 'child_of', int(cat.id))])
            category_count[str(cat.id)] = search_product
        return category_count

    # =====================================================================================================================================
    # =====================================================================================================================================
    @http.route('/get/quick_modal_data_ids', type='json', auth='public', website=True, sitemap=False)
    def get_json_modal_data(self, dataList, dataType, **post):
        if dataType == "brand":
            dataList = json.loads(dataList)
            common_domain = [('active','=',True), ('website_id', 'in', (False, request.website.id))]
            all_brand_list = request.env['as.product.brand'].search([('id','in',dataList)] + common_domain)
            modal_brand_list = [[brand.name.title(),brand.id] for brand in all_brand_list]
            modal_brand_list.sort(key=lambda x:x[0])
            curr_alpha = []
            for res in modal_brand_list:
                if res[0][0] not in curr_alpha:
                    curr_alpha.append(res[0][0])
            result = {'modal_data_list': modal_brand_list, 'curr_alpha':curr_alpha}
            return result
        elif dataType == "category":
            dataList = json.loads(dataList)
            website_domain = request.website.website_domain()
            categs = request.env['product.public.category'].search([('id', 'in', dataList)] + website_domain)
            modal_cat_list = [[cat.name.title(),cat.id] for cat in categs]
            modal_cat_list.sort(key=lambda x:x[0])
            curr_alpha = []
            for res in modal_cat_list:
                if res[0][0] not in curr_alpha:
                    curr_alpha.append(res[0][0])
            result = {'modal_data_list': modal_cat_list, 'curr_alpha':curr_alpha}
            return result

    @http.route('/get/quick_modal_data', type='json', auth='public', website=True)
    def quick_search_modal_data(self, **kwargs):
        counter = False
        no_prod = False
        selData = kwargs.get('selData')
        alphabets = kwargs.get('alphabets')
        dataType = kwargs.get('dataType')
        dataList = kwargs.get('dataList')
        prod_count = kwargs.get('prod_count')
        curr_alpha = kwargs.get('curr_alpha')
        if selData == None:
            selData = []
        if kwargs.get('counter'):
            counter = kwargs.get('counter')
        if kwargs.get('no_prod'):
            no_prod = kwargs.get('no_prod')
        active_list = []
        for dta in dataList:
            if no_prod and (prod_count[str(dta[1])] != 0):
                if dta[0][0] not in active_list:
                    if dta[0][0] not in alphabets:
                        active_list.append('#')
                    else:
                        active_list.append(dta[0][0])

        get_template = request.env['ir.ui.view']._render_template(
            "atharva_theme_base.qck_search_modal", {'alphabets': alphabets,
            'dataType': dataType, 'dataList': dataList,
            'counter': counter, 'prod_count': prod_count,
            'no_prod': no_prod, 'selData': selData,
            'curr_alpha':curr_alpha, 'active_list':active_list})
        return {'template': get_template}

    @http.route([])
    def product(self, product, category='', search='', **kwargs):
        res = super(AtharvaWebsiteSaleExtend, self).product(product, category, search, **kwargs)
        res.qcontext.update({'as_product_detail':True})
        return res

    @http.route(['/shop/brands'], type='http', auth="public", website=True)
    def ProductBrands(self, *post):
        domain = ['&',('active','=',True), ('website_id', 'in', (False, request.website.id))]
        brand_letters = []
        initials = []
        brands = request.env['as.product.brand'].sudo().search(domain, order="name asc")
        for brand in brands:
            if brand.name[0].upper() not in brand_letters:
                brand_letters.append(brand.name[0].upper())
        initials = brand_letters.copy()
        for i in list(string.ascii_uppercase):
            if i not in initials:
                initials.append(i)
        values = {
            'brand_letters' : brand_letters,
            'initials':sorted(initials)
        }
        return request.render("atharva_theme_base.product_brands", values)

    @http.route(['/shop/cart'], type='http', auth="public", website=True)
    def cart(self, **post):
        if request.website.active_b2b and request.env.user._is_public():
            raise NotFound
        res = super(AtharvaWebsiteSaleExtend, self).cart(**post)
        return res