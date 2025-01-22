odoo.define('theme_alan.s_product_offer_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const productDialog = require('theme_alan.productDialog');
const webUtils = require('web.utils');

options.registry.AsProductOffer= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/product_offer_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-offer-config':'_product_offer_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._product_offer_configure();
    },
    _product_offer_configure: function(){
        let cr = this;
        const prodOfferData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_product_offer_modal",{'type': 'offer'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            initRecords:cr.$target.attr("data-prod-ids"),
            offerTime:cr.$target.attr("data-offerTime"),
            imgPosition:cr.$target.attr("data-imgPosition"),
            cart:cr.$target.attr("data-cart"),
            buyNow:cr.$target.attr("data-buyNow"),
            prodLabel:cr.$target.attr("data-prodLabel"),
            rating:cr.$target.attr("data-rating"),
            popupType:"Product Offer",
        }
        cr.productDialog = new productDialog(cr, prodOfferData);
        cr.productDialog.open();
    },
    cleanForSave: function () {
        this.$target.addClass("d-none").empty();
    },
});
});