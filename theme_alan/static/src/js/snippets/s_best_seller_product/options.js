odoo.define('theme_alan.s_best_seller_product_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const productDialog = require('theme_alan.productDialog');
const webUtils = require('web.utils');

options.registry.AsBestSellerProduct= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/product_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-best-prod-config':'_best_product_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._best_product_configure();
    },
    _best_product_configure: function(){
        let cr = this;
        const bestProdData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_product_modal", {'type': 'best_product'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            mainUI:cr.$target.attr("data-mainUI"),
            totalCount:cr.$target.attr("data-totalCount"),
            styleUI:cr.$target.attr("data-styleUI"),
            autoSlider:cr.$target.attr("data-autoSlider"),
            dataCount:cr.$target.attr("data-dataCount"),
            sTimer:cr.$target.attr("data-sTimer"),
            cart:cr.$target.attr("data-cart"),
            quickView:cr.$target.attr("data-quickView"),
            compare:cr.$target.attr("data-compare"),
            wishList:cr.$target.attr("data-wishList"),
            prodLabel:cr.$target.attr("data-prodLabel"),
            rating:cr.$target.attr("data-rating"),
            infinity:cr.$target.attr("data-infinity"),
            slider:cr.$target.attr("data-slider"),
            popupType:"Best Product",
        }
        cr.productDialog = new productDialog(cr, bestProdData);
        cr.productDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },
});
});