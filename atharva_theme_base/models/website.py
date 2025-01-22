# -*- coding: utf-8 -*-

from markupsafe import Markup
from odoo import fields, models, api
from odoo.exceptions import UserError

class CustomWebsite(models.Model):
    _inherit = 'website'

    is_alan = fields.Boolean(string="Is theme Alan?", compute="_is_theme_alan", default=False)
    categ_search_active = fields.Boolean(string="Category Search", help='Enable to activate advance category search.')
    attr_search_active = fields.Boolean(string="Attribute Search", help='Enable to activate advance attribute search.')
    brand_search_active = fields.Boolean(string="Brand Search", help='Enable to activate advance brand search.')
    tag_search_active = fields.Boolean(string="Tag Search", help='Enable to activate advance tag search.')
    categories_to_show = fields.Integer(string='Number of Categories', store=True)
    attributes_to_show = fields.Integer(string='Number of Attributes', store=True)
    brands_to_show = fields.Integer(string='Number of Brands', store=True)
    tags_to_show = fields.Integer(string='Number of Tags', store=True)
    active_b2b = fields.Boolean(string="Enable B2B")

    def get_website_faq_list(self):
        faqs = self.env['faq'].sudo().search([('website_id', 'in', (False, self.get_current_website().id)),
        ('is_published', '=', True)])
        faqs = [{'fid':f.id,'question':f.question, 'answer':Markup(f.answer)} for f in faqs]
        return faqs

    @api.depends('theme_id')
    def _is_theme_alan(self):
        for site in self:
            theme = site.theme_id.name
            if theme == "theme_alan":
                site.is_alan = True
            else:
                site.is_alan = False
                site.categ_search_active = False
                site.brand_search_active = False
                site.attr_search_active = False
                site.tag_search_active = False

class ThemeUtilsExtend(models.AbstractModel):
    _inherit = 'theme.utils'

    @api.model
    def _reset_default_config(self):
        # Reinitialize some css customizations
        self.env['web_editor.assets'].make_scss_customization(
            '/website/static/src/scss/options/user_values.scss',
            {
                'font': 'null',
                'headings-font': 'null',
                'navbar-font': 'null',
                'buttons-font': 'null',
                'color-palettes-number': 'null',
                'color-palettes-name': 'null',
                'btn-ripple': 'null',
                'header-template': 'null',
                'footer-template': 'null',
                'footer-scrolltop': 'null',
            }
        )

        # Reinitialize effets
        self.disable_asset('website.ripple_effect_scss')
        self.disable_asset('website.ripple_effect_js')
        # custom header
        self.disable_view('website.template_header_hamburger')
        self.disable_view('website.template_header_vertical')
        self.disable_view('website.template_header_sidebar')
        self.disable_view('website.template_header_slogan')
        self.disable_view('website.template_header_contact')
        self.disable_view('website.template_header_boxed')
        self.disable_view('website.template_header_centered_logo')
        self.disable_view('website.template_header_image')
        self.disable_view('website.template_header_hamburger_full')
        self.disable_view('website.template_header_magazine')
        self.disable_view('website.template_header_default')
        self.enable_view('atharva_theme_base.atharva_header')

        # custom footer
        self.disable_view('website.template_footer_descriptive')
        self.disable_view('website.template_footer_centered')
        self.disable_view('website.template_footer_links')
        self.disable_view('website.template_footer_minimalist')
        self.disable_view('website.template_footer_contact')
        self.disable_view('website.template_footer_call_to_action')
        self.disable_view('website.template_footer_headline')
        self.disable_view('website.footer_custom')
        self.enable_view('atharva_theme_base.atharva_footer')
        # Reinitialize footer scrolltop template
        self.disable_view('website.option_footer_scrolltop')

class WebsiteMenuAlanTags(models.Model):
    _inherit = "website.menu"

    is_tag_active = fields.Boolean(string="Menu Tag")
    tag_text_color = fields.Char(string="Tag Text Color")
    tag_bg_color = fields.Char(string="Tag Background Color")
    tag_text = fields.Char(string="Tag Text", translate=True)

    hlt_menu = fields.Boolean(string="Highlight Menu")
    hlt_menu_bg_color = fields.Char(string="Background Color")
    hlt_menu_ft_col = fields.Char(string="Font Color")
    hlt_menu_icon = fields.Binary(string="Icon")

class QckSearchConfigs(models.TransientModel):
    _inherit = "res.config.settings"

    is_alan = fields.Boolean(string="Is theme Alan", related="website_id.is_alan")
    categ_search_active = fields.Boolean(string='Activate Advance Category Search', related='website_id.categ_search_active', readonly=False, help='Enable to activate advance category search.')
    attr_search_active = fields.Boolean(string='Activate Advance Attribute Search', related='website_id.attr_search_active', readonly=False, help='Enable to activate advance attribute search.')
    brand_search_active = fields.Boolean(string='Activate Advance Brand Search', related='website_id.brand_search_active', readonly=False, help='Enable to activate advance brand search.')
    tag_search_active = fields.Boolean(string='Activate Advance Tag Search', related='website_id.tag_search_active', readonly=False, help='Enable to activate advance tag search.')
    categories_to_show = fields.Integer(string='Number of Categories', related='website_id.categories_to_show', readonly=False)
    attributes_to_show = fields.Integer(string='Number of Attributes', related='website_id.attributes_to_show', readonly=False)
    brands_to_show = fields.Integer(string='Number of Brands', related='website_id.brands_to_show', readonly=False)
    tags_to_show = fields.Integer(string='Number of Tags', related='website_id.tags_to_show', readonly=False)
    active_b2b = fields.Boolean(string='Enable B2B', related='website_id.active_b2b', readonly=False)

    @api.constrains('categories_to_show', 'attributes_to_show', 'brands_to_show', 'tags_to_show')
    def quick_search_validation(self):
        for filter_opt in self:
            if filter_opt.categ_search_active:
                if filter_opt.categories_to_show <= 0:
                    raise UserError('Category count should be more than 0.')
            if filter_opt.attr_search_active:
                if filter_opt.attributes_to_show <= 0:
                    raise UserError('Attribute count should be more than 0.')
            if filter_opt.brand_search_active:
                if filter_opt.brands_to_show <= 0:
                    raise UserError('Brand count should be more than 0.')
            if filter_opt.tag_search_active:
                if filter_opt.tags_to_show <= 0:
                    raise UserError('Tag count should be more than 0.')