# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.tools.translate import html_translate

class ProductBrand(models.Model):
    _name = 'as.product.brand'
    _inherit = ['website.multi.mixin', 'website.searchable.mixin',]
    _description = 'Product Brands'
    _order = "sequence,id"

    sequence = fields.Integer(string='Sequence')
    name = fields.Char(string='Brand Name', translate=True, required=True)
    logo = fields.Binary(string='Logo', required=True)
    visible_slider = fields.Boolean(string='Visible in Website', default=True)
    active = fields.Boolean(string='Active', default=True)
    brand_description = fields.Text(string='Description', translate=True)
    description = fields.Html(string='Website Description', translate=html_translate)
    brand_product_ids = fields.One2many('product.template','product_brand_id', string='Brand Products',)
    products_count = fields.Integer(string='Number of products', compute='_get_products_count')

    def get_brands(self, letter=False):
        res = []
        if letter:
            brand_list = []
            brands = self.search([])
            for brand in brands:
                brand_list.append(brand)
            for idx in brand_list:
                res = [idx for idx in brand_list if idx.name[0].lower() == letter.lower()]
        return res

    _sql_constraints = [('name_uniqe', 'unique (name)',
                         "Brand name already exists.!")]


    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        results_data = super()._search_render_results(fetch_fields, mapping, icon, limit)
        for data in results_data:
            data['url'] = '/shop?brand=%s' % data['id']
        return results_data

    @api.depends('brand_product_ids')
    def _get_products_count(self):
        ''' Product count brandwise '''
        self.products_count = len(self.brand_product_ids)

    def as_get_brand_product(self):
        ''' Brand page redirector '''
        result = {
            "type": "ir.actions.act_window",
            "res_model": "product.template",
            "domain": [['product_brand_id', '=', self.id]],
            "name": "Products",
            'view_mode': 'kanban,tree,form',
        }
        return result

class ASProductTemplateExtend(models.Model):
    _inherit = 'product.template'

    product_brand_id = fields.Many2one('as.product.brand', string='Brand', help='Select a brand for this product')