# -*- coding: utf-8 -*-


from odoo import fields, models
from odoo.tools.translate import html_translate

class AlanAdvanceSearch(models.Model):
    _inherit = 'website'

    shop_special_offer = fields.Html(sanitize_form=False, sanitize_attributes=False, translate=html_translate)

    def _search_get_details(self, search_type, order, options):
        result = super()._search_get_details(search_type, order, options)
        if search_type == "as_advance_search":
            result.append(self._alan_category_search(order, options))
            result.append(self._alan_brand_search(order, options))
            result.append(self._alan_tags_search(order, options))
            result.append(self._alan_product_search(order, options))
        return result

    def _alan_category_search(self, order, options):
        data = self.env['product.public.category']._search_get_detail(self, order, options)
        data.update({'data_type':'category'})
        return data

    def _alan_product_search(self, order, options):
        data = self.env['product.template'].sudo()._search_get_detail(self, order, options)
        data.update({'data_type':'products'})
        return data

    def _alan_brand_search(self, order, options):
        search_fields = ['name']
        fetch_fields = ['id', 'name']
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'website_url': {'name': 'url', 'type': 'text'},
        }
        return {
            'data_type':'brand',
            'model': 'as.product.brand',
            'base_domain': [], # categories are not website-specific
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'brand',
            'order': 'name desc, id desc' if 'name desc' in order else 'name asc, id desc',
        }
    def _alan_tags_search(self, order, options):
        search_fields = ['name']
        fetch_fields = ['id', 'name']
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'website_url': {'name': 'url', 'type': 'text'},
        }
        return {
            'data_type':'tag',
            'model': 'product.tags',
            'base_domain': [], # categories are not website-specific
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'tag',
            'order': 'name desc, id desc' if 'name desc' in order else 'name asc, id desc',
        }

class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    pv_thumbnail = fields.Image('Variant Image')
