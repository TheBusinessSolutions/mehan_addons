odoo.define('theme_alan.s_categ_product_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const catProductDialog = require('theme_alan.catProductDialog');
const webUtils = require('web.utils');

options.registry.AsCategProduct= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/categ_product_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-categ-prod-config':'_categ_prod_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._categ_prod_configure('click');
    },
    _categ_prod_configure: function(){
        let cr = this;
        const categData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_categ_product_modal", {'type': 'categ_product'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            initRecords:cr.$target.attr("data-prod-ids"),
            catRecords:cr.$target.attr("data-cat-ids"),
            styleUI:cr.$target.attr("data-styleUI"),
            autoSlider:cr.$target.attr("data-autoSlider"),
            sTimer:cr.$target.attr("data-sTimer"),
            cart:cr.$target.attr("data-cart"),
            quickView:cr.$target.attr("data-quickView"),
            compare:cr.$target.attr("data-compare"),
            wishList:cr.$target.attr("data-wishList"),
            prodLabel:cr.$target.attr("data-prodLabel"),
            rating:cr.$target.attr("data-rating"),
            infinity:cr.$target.attr("data-infinity"),
            slider:cr.$target.attr("data-slider"),
            popupType:"Categ Product",
        }
        cr.catProductDialog = new catProductDialog(cr, categData);
        cr.catProductDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },
});
});