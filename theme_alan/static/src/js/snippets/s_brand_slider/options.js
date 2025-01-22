odoo.define('theme_alan.s_brand_slider_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const brandCatDialog = require('theme_alan.brandCatDialog');
const webUtils = require('web.utils');

options.registry.AsBrandSlider= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/cat_brand_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-brand-config':'_brand_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._brand_configure();
    },
    _brand_configure: function(){
        let cr = this;
        const brandData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_brand_modal", {'type': 'brand'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            initRecords:cr.$target.attr("data-brand-ids"),
            mainUI:cr.$target.attr("data-mainUI"),
            styleUI:cr.$target.attr("data-styleUI"),
            recordLink:cr.$target.attr("data-recordLink"),
            recordName:cr.$target.attr("data-recordName"),
            autoSlider:cr.$target.attr("data-autoSlider"),
            dataCount:cr.$target.attr("data-dataCount"),
            sTimer:cr.$target.attr("data-sTimer"),
            slider:cr.$target.attr("data-slider"),
            popupType:"Brand",
        }
        cr.brandCatDialog = new brandCatDialog(cr, brandData);
        cr.brandCatDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },
});
});