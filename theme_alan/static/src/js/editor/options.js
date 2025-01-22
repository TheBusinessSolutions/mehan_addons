odoo.define('theme_alan.as_snippet as-load_option_editor', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const megaDialog = require('theme_alan.core_mega_dialog');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const webUtils = require('web.utils');

options.registry.AsDynamicMegaMenu = options.Class.extend(BaseAlanQweb, {
    xmlDependencies: [ '/theme_alan/static/src/xml/core_dialog.xml',
        '/theme_alan/static/src/xml/megamenu/product_mega_modal.xml',
        '/theme_alan/static/src/xml/megamenu/category_mega_modal.xml'],
    events:{'click .set-mega-config':'_open_megamenu_config' },
    _open_megamenu_config:function(){
        var cr = this;
        const megaData = {
            title:"Configuration",
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb(cr.$target.data("megaPopup"),{'title':cr.$target.data("megaTitle"),
            'megaView':cr.$target.data("catMegaView") || cr.$target.data("prodMegaView")})).html()),
            initRecords:cr.$target.data("recordIds"),
            catSeq:cr.$target.data("catSeq"),
            megaUi:cr.$target.data("megaUi"),
            colUi:cr.$target.data("colUi"),
            fullSubTemplate:1,
            enableCoreButton:0,
            megaPopup:cr.$target.data("megaPopup"),
            enableCoreTitle:0
        }
        cr.megaDialog = new megaDialog(cr, megaData);
        cr.megaDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },

});

});