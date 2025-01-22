# -*- coding: utf-8 -*-

import json
import logging

from odoo import http, _
from odoo.http import request
from odoo.osv import expression

_logger = logging.getLogger(__name__)

class ThemeAlanBaseFeatureRoute(http.Controller):
    def _fetchBasicProdData(self, products, **kwargs):
        ''' Common method to fetch core product data'''
        res_data = []
        for prod in products:
            sign_prod = {}
            if prod.description_sale and len(prod.description_sale) > 100:
                desc = prod.description_sale[:100] + "..."
            else:
                desc = prod.description_sale or ""
            if kwargs.get('is_variant') == False:
                sign_prod.update({"id":prod.id,
                    "name":prod.name, "display_name": prod.display_name,
                    "image": request.website.image_url(prod,"image_512"),
                    "description":desc, "access_link":f"/shop/product/{prod.id}"
                })
            else:
                sign_prod.update({"id":prod.id,
                    "name":prod.display_name, "display_name": prod.display_name,
                    "image": request.website.image_url(prod,"image_512"),
                    "description":desc, "access_link":f"/shop/product/{prod.id}"
                })
            res_data.append(sign_prod)
        return res_data

    def _fetchBasicCatData(self, categories):
        ''' Common method to fetch core category data'''
        res_data = []
        for cat in categories:
            sign_cat = {}
            sign_cat.update({
                "id":cat.id, "name":cat.name,
                "display_name": cat.display_name,
                "image": request.website.image_url(cat,"image_512"),
                "access_link":f"/shop/?category={cat.id}"
            })
            res_data.append(sign_cat)
        return res_data

    def _fetchBasicBrandData(self, brands):
        ''' Method to fetch core brand data'''
        res_data = []
        for brand in brands:
            sign_brand = {}
            sign_brand.update({
                "id":brand.id,
                "name":brand.name,
                "logo":request.website.image_url(brand,"logo")
            })
            res_data.append(sign_brand)
        return res_data

    def _fetchBasicBlogData(self, blogs):
        ''' Method to fetch blog data'''
        res_data = []
        for blog in blogs:
            sign_blog = {}
            sign_blog.update({
                "id":blog.id,
                "name":blog.name,
                "author_name":blog.author_name
            })
            res_data.append(sign_blog)
        return res_data

    def _alanDataGetter(self, dataMethod=False, extra_field=[], limit=10, domain=[], **kwargs):
        ''' Method to get core data for all select2 dialog box'''
        if dataMethod == "select2_product":
            products = request.env["product.template"].sudo().search(domain, limit=limit)
            return self._fetchBasicProdData(products, is_variant=False)
        elif dataMethod == "select2_category":
            categories = request.env["product.public.category"].search(domain, limit=limit)
            return self._fetchBasicCatData(categories)
        elif dataMethod == "select2_brand":
            brands = request.env["as.product.brand"].search(domain, limit=limit)
            return self._fetchBasicBrandData(brands)
        elif dataMethod == "select2_product_variant":
            products = request.env["product.product"].sudo().search(domain, limit=limit)
            return self._fetchBasicProdData(products, is_variant=True)
        elif dataMethod == "select2_blog":
            blogs = request.env["blog.post"].search(domain, limit=limit)
            return self._fetchBasicBlogData(blogs)

    @http.route("/alan_template_getter", type="json", auth="public", website=True)
    def alanTemplateGetters(self,**kwargs):
        ''' Method fetch any module template with context'''
        template = kwargs.get("template",False)
        context = kwargs.get("data",False)
        default = {"template":"<h2>No Template Found!</h2>"}
        if template:
            try:
                template = request.env["ir.ui.view"]._render_template(template,context)
                return {"template":template}
            except Exception as e:
                _logger.warning(e)
                return default
        return default

    @http.route("/get/select2/data", type="http", auth="public", website=True, sitemap=False)
    def getSelect2Data(self, searchType=False, **kwargs):
        ''' Method to get all select2 data'''
        typeLst = [ "Category", "SubCategoryLevel1",]
        if searchType in [ "Product", "ImageHotspot", "CatProdGrid", "CategProd", "ProdOffer"]:
            searchTerm = [("is_published","=",True),("name", "ilike", (kwargs.get("searchTerm") or ""))]
            if searchType in ["CatProdGrid", "CategProd"]:
                if kwargs.get("parentDomain") == "false":
                    parent_id = False
                else:
                    parent_id = int(kwargs.get("parentDomain"))
                parentDomain = [('public_categ_ids','=', parent_id )]
                domain = expression.AND([request.website.website_domain(), searchTerm, parentDomain])
            else:
                domain = expression.AND([request.website.website_domain(), searchTerm])
            records = self._alanDataGetter(dataMethod="select2_product", domain=domain, limit=15)
        elif searchType == "Product Variant":
            searchTerm = [("is_published","=",True),("name", "ilike", (kwargs.get("searchTerm") or ""))]
            domain = expression.AND([request.website.website_domain(), searchTerm])
            records = self._alanDataGetter(dataMethod="select2_product_variant", domain=domain, limit=15)
        elif searchType in typeLst:
            if kwargs.get("parentDomain") == "false":
                parent_id = False
            else:
                parent_id = int(kwargs.get("parentDomain"))
            parentDomain = [('parent_id','=', parent_id )]
            searchTerm = [("name", "ilike", (kwargs.get("searchTerm") or ""))]
            domain = expression.AND([request.website.website_domain(), searchTerm, parentDomain])
            records = self._alanDataGetter(dataMethod="select2_category", domain=domain, limit=15)
        elif searchType == "BrandMix":
            searchTerm = [("name", "ilike", (kwargs.get("searchTerm") or ""))]
            domain = expression.AND([request.website.website_domain(), searchTerm])
            records = self._alanDataGetter(dataMethod="select2_brand", domain=domain, limit=15)
        elif searchType in ["CatMix", "CatProds", "CatGrid"]:
            searchTerm = [("name", "ilike", (kwargs.get("searchTerm") or ""))]
            domain = expression.AND([request.website.website_domain(), searchTerm])
            records = self._alanDataGetter(dataMethod="select2_category", domain=domain, limit=15)
        elif searchType == "Blogs":
            searchTerm = [("name", "ilike", (kwargs.get("searchTerm") or ""))]
            domain = expression.AND([request.website.website_domain(), searchTerm])
            records = self._alanDataGetter(dataMethod="select2_blog", domain=domain, limit=15)
        return json.dumps(records)

    @http.route("/get/product/raw/data", type="json", auth="public", website=True)
    def alanProductRawData(self, product_ids, model):
        ''' Method to fatch product variant and product template data'''
        if type(product_ids) == str:
                product_ids = json.loads(product_ids)
        website_domain = request.website.website_domain()
        if product_ids:
            prod_ids = [int(prod_id) for prod_id in product_ids]
            prod_vals = request.env[model].search(["&", ("is_published","=",True), ("sale_ok","=", True), ("id", "in", prod_ids)] + website_domain)
            seq_prod = []
            for prod_id in prod_ids:
                for prod in prod_vals.ids:
                    if prod_id == prod:
                        seq_prod.append(prod)
                        break
            products = request.env[model].browse(seq_prod)
            if model == "product.template":
                return self._fetchBasicProdData(products, is_variant=False)
            else:
                return self._fetchBasicProdData(products, is_variant=True)

    @http.route("/get/category/raw/data", type="json", auth="public", website=True)
    def alanCategoryRawData(self, category_ids):
        ''' Method to fatch product variant and product template data'''
        website_domain = request.website.website_domain()
        if category_ids:
            if type(category_ids) == str:
                category_ids = json.loads(category_ids)
            seq_categ = []
            for c in category_ids:
                get_categ = request.env['product.public.category'].search([('id','=',c)] + website_domain)
                if len(get_categ):
                    seq_categ.append(get_categ.id)
            categories = request.env['product.public.category'].browse(seq_categ)
            return self._fetchBasicCatData(categories)

    @http.route("/get/brand/raw/data", type="json", auth="public", website=True)
    def alanBrandRawData(self, brand_ids):
        if brand_ids:
            if type(brand_ids) == str:
                brand_ids = json.loads(brand_ids)
            website_domain = request.website.website_domain()
            brand_lst = []
            for b in brand_ids:
                get_brand = request.env['as.product.brand'].search([('id','=',b)] + website_domain)
                if len(get_brand):
                    brand_lst.append(get_brand.id)
            brands = request.env["as.product.brand"].browse(brand_lst)
            return self._fetchBasicBrandData(brands)

    @http.route("/get/blog/raw/data", type="json", auth="public", website=True)
    def alanBlogRawData(self, blog_ids):
        website_domain = request.website.website_domain()
        if blog_ids:
            if type(blog_ids) == str:
                blog_ids = json.loads(blog_ids)
            seq_blog = []
            for b in blog_ids:
                get_blog = request.env['blog.post'].search([('id','=',b)] + website_domain)
                if len(get_blog):
                    seq_blog.append(get_blog.id)
            blogs = request.env['blog.post'].browse(seq_blog)
            return self._fetchBasicBlogData(blogs)

    @http.route("/get/category/mega/template", type="json", auth="public", website=True)
    def alanCategoryMegaTemplate(self, **kwargs):
        ''' Method to fetch mega menu template '''
        view = kwargs.get("view", False)
        category_data = kwargs.get("category_data", False)
        category_ids = kwargs.get("category_ids", False)
        category_ui = kwargs.get("category_ui", False)
        column_ui = kwargs.get("column_ui", False)
        website_domain = request.website.website_domain()
        data = {}
        seq_category_data = {}
        if type(category_ids) == str:
            category_ids = json.loads(category_ids)
        if type(category_data) == str:
            category_data = json.loads(category_data)
        for i in category_ids:
            val = category_data[str(i)]
            perent_id = request.env["product.public.category"].search([('id','=',i)] + website_domain);
            sub_cat_ids = request.env["product.public.category"].browse(val[1]);
            sub_vals = []
            for sc in val[1]:
                sub_categs = request.env["product.public.category"].search([('id','=',sc)] + website_domain);
                if len(sub_categs) == 1:
                    sub_vals.append(sub_categs.id)
            sub_cat_ids = request.env["product.public.category"].browse(sub_vals);
            data.update({perent_id:sub_cat_ids})
            seq_category_data.update({str(i):val})
        if view == "grid":
            temp_name = "atharva_theme_base.as_mm_category_grid"
        else:
            temp_name = "atharva_theme_base.as_mm_category_list"
        template = request.env["ir.ui.view"]._render_template(temp_name,
        {"cat_data":data,"mega_ui":category_ui,"col_ui":column_ui,"is_dynamic":True,
        'cat_ids':seq_category_data,'cat_seq':category_ids})
        return {'template':template}

    @http.route("/shop/mini/cart", type="json", auth="public", website=True)
    def _alan_mini_cart(self):
        ''''Mini Cart Template Getter '''
        context = {'website_sale_order': request.website.sale_get_order()}
        template = request.env["ir.ui.view"]._render_template("atharva_theme_base.cart_lines_popup_content", context)
        return {"template":template }
