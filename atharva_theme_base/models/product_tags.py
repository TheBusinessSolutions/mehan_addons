# -*- coding: utf-8 -*-

from odoo import fields, models, api

class ProductTags(models.Model):
    _name = "product.tags"
    _inherit = ['website.searchable.mixin',]
    _description = "Product Tags"
    _order = "sequence, id"

    name = fields.Char(required=True, translate=True)
    active = fields.Boolean(default=True, help="The active field allows you to hide the tag without removing it.")
    sequence = fields.Integer(help="Gives the sequence order when displaying a list of rules.")
    product_ids = fields.Many2many('product.template', string='Products')
    website_id = fields.Many2one('website', string='Website')

    _sql_constraints = [('unique_tag_name', 'unique (name)',"Tag already exists!")]

    def _search_render_results(self, fetch_fields, mapping, icon, limit):
        results_data = super()._search_render_results(fetch_fields, mapping, icon, limit)
        for data in results_data:
            data['url'] = '/shop?tag=%s' % data['id']
        return results_data

class ProductTemplateTagExtend(models.Model):
    _inherit = 'product.template'

    product_tags_ids = fields.Many2many('product.tags', string='Product Tags')

    def _getTags(self, product):
        ''' Product tag template getter in popover on shop page'''
        if product.product_tags_ids:
            tag_html = ""
            for tag in product.product_tags_ids:
                tag_html += f"<div class='as-parent-tag'>{tag.name}</div>"
            return tag_html