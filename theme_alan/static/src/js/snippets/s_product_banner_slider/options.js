odoo.define('theme_alan.s_product_banner_slider_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const webUtils = require('web.utils');
const productDialog = require('theme_alan.productDialog');

options.registry.AsProductBannerSlider= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/product_banner_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-prod-banner-config':'_product_banner_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._product_banner_configure();
    },
    _product_banner_configure: function(){
        var cr = this;
        var prodBannerData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_product_banner_modal",{'type': 'banner'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            initRecords:cr.$target.attr("data-prod-ids"),
            imgPosition:cr.$target.attr("data-imgPosition"),
            autoSlider:cr.$target.attr("data-autoSlider"),
            sTimer:cr.$target.attr("data-sTimer"),
            cart:cr.$target.attr("data-cart"),
            buyNow:cr.$target.attr("data-buyNow"),
            prodLabel:cr.$target.attr("data-prodLabel"),
            rating:cr.$target.attr("data-rating"),
            infinity:cr.$target.attr("data-infinity"),
            slider:cr.$target.attr("data-slider"),
            popupType:"Product Banner",
        };
        cr.productDialog = new productDialog(cr, prodBannerData);
        cr.productDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },
});
});