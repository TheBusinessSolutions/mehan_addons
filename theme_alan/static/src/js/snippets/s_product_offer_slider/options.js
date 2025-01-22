odoo.define('theme_alan.s_product_offer_slider_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const offerDialog = require('theme_alan.offerDialog');
const webUtils = require('web.utils');

options.registry.AsProdOfferSlider= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/offer_slider_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-offer-slider-config':'_product_offer_slider_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._product_offer_slider_configure();
    },
    _product_offer_slider_configure: function(){
        let cr = this;
        const prodOfferData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_offer_slider_modal",{'type': 'offer_slider'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            initRecords:cr.$target.attr("data-prod-ids"),
            TimerData:cr.$target.attr("data-timerData"),
            imgPosition:cr.$target.attr("data-imgPosition"),
            mainUI:cr.$target.attr("data-mainUI"),
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
            popupType:"Offer Slider",
        }
        cr.offerDialog = new offerDialog(cr, prodOfferData);
        cr.offerDialog.open();
    },
    cleanForSave: function () {
        this.$target.addClass("d-none").empty();
    },
});
});