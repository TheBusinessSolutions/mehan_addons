odoo.define('theme_alan.s_categ_grid_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const catGridDialog = require('theme_alan.catGridDialog');
const webUtils = require('web.utils');

options.registry.AsCategGrid= options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/category_grid_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-categ-grid-config':'_categ_grid_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._categ_grid_configure('click');
    },
    _categ_grid_configure: function(){
        let cr = this;
        const categData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_categ_grid_modal", {'type': 'categ_grid'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            initRecords:cr.$target.attr("data-cat-ids"),
            prodRecords:cr.$target.attr("data-prod-ids"),
            styleUI:cr.$target.attr("data-styleUI"),
            dataCount:cr.$target.attr("data-dataCount"),
            popupType:"Categ Product",
        }
        cr.catGridDialog = new catGridDialog(cr, categData);
        cr.catGridDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },
});
});