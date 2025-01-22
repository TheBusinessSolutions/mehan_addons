odoo.define('theme_alan.s_cat_slider_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const brandCatDialog = require('theme_alan.brandCatDialog');
const webUtils = require('web.utils');

options.registry.AsCategorySlider= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/cat_brand_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-cat-config':'_cat_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._cat_configure('click');
    },
    _cat_configure: function(){
        let cr = this;
        const catData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_cat_modal", {'type': 'category'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            initRecords:cr.$target.attr("data-cat-ids"),
            mainUI:cr.$target.attr("data-mainUI"),
            styleUI:cr.$target.attr("data-styleUI"),
            recordLink:cr.$target.attr("data-recordLink"),
            autoSlider:cr.$target.attr("data-autoSlider"),
            dataCount:cr.$target.attr("data-dataCount"),
            sTimer:cr.$target.attr("data-sTimer"),
            slider:cr.$target.attr("data-slider"),
            popupType:"Category",
        }
        cr.brandCatDialog = new brandCatDialog(cr, catData);
        cr.brandCatDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },
});
});