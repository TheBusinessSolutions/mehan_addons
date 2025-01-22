# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.translate import html_translate

class ASProductTemplateExtend(models.Model):
    _inherit = 'product.template'

    product_rating = fields.Float(string='Product Rating', compute='_compute_product_rating', store=True)
    product_tab_description = fields.Html(string="Description Tab", translate=html_translate)
    product_offer_ids = fields.Many2many("as.product.extra.info", string="Offers")
    hover_image = fields.Binary("Hover Image")
    doc_name = fields.Char(string="Tab Name", default='Documents', required=True)
    is_active_doc = fields.Boolean(default=False, string='Show Document')
    doc_attachments = fields.Many2many("ir.attachment", string="Documents")

    @api.model
    def create(self, vals):
        if vals.get('doc_attachments'):
            doc_list = [i for i in vals['doc_attachments'][0][2]]
            attachments = self.env['ir.attachment'].sudo().browse(doc_list)
            for record in attachments:
                if record.id in doc_list:
                    if record.public == False:
                        record.public = True
        return super(ASProductTemplateExtend, self).create(vals)

    def write(self, vals):
        if vals.get('doc_attachments'):
            doc_list = [i for i in vals['doc_attachments'][0][2]]
            attachments = self.env['ir.attachment'].sudo().browse(doc_list)
            for record in attachments:
                if record.id in doc_list:
                    if record.public == False:
                        record.public = True
        return super(ASProductTemplateExtend, self).write(vals)

    @api.depends('message_ids')
    def _compute_product_rating(self):
        ''' Compute product rating '''
        for i in self:
            prodRating = round(i.sudo().rating_get_stats().get('avg') / 1 * 100) / 100
            i.product_rating = prodRating

    @api.model
    def _search_get_detail(self, website, order, options):
        ''' Add RBT domain '''
        res = super(ASProductTemplateExtend,self)._search_get_detail(website=website, order=order, options=options)
        base_domain = res.get("base_domain")
        if self.env.context.get("rating",[]) != []:
            min_rating = min(self.env.context.get("rating",[0]))
            base_domain.append([('product_rating','>=', min_rating)])
            res.update({"base_domain":base_domain})
        if self.env.context.get("brands",False):
            base_domain.append([('product_brand_id','in',[int(i) for i in self.env.context.get("brands",[])])])
            res.update({"base_domain":base_domain})
        if self.env.context.get("tags",False):
            base_domain.append([('product_tags_ids','in',[int(i) for i in  self.env.context.get("tags",[])])])
            res.update({"base_domain":base_domain})
        return res