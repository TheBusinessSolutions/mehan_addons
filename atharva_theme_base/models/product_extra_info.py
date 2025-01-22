# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools.translate import html_translate

class ProductOffer(models.Model):
    _name = "as.product.extra.info"
    _description = "Product Extra Information"

    sequence = fields.Integer(string="Sequence")
    types = fields.Selection([('offer','Offer'),('attrib','Attribute')], required=True)
    icon = fields.Char(default="tags")
    name = fields.Char(translate=True, required=True)
    short_description = fields.Char(string="Description", translate=True)
    detail_description = fields.Html(translate=html_translate, sanitize_form=False, sanitize_attributes=False)
    product_ids = fields.Many2many("product.template", string="Products")

    def as_product_info_design(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': '/offers/editor/%s?enable_editor=1' % (self.id),
            'target': 'new',
        }

class ProductAttributeExtend(models.Model):
    _inherit = 'product.attribute'

    attribute_extra_info_id = fields.Many2one("as.product.extra.info",
        string="Show Extra Info", domain='[("types", "=", "attrib")]')