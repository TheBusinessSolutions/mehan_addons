odoo.define('theme_alan.s_gallery_image_options', function (require) {
"use strict";

const options = require('web_editor.snippets.options');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const brandCatDialog = require('theme_alan.brandCatDialog');
const webUtils = require('web.utils');

options.registry.AsGalleryImage= options.Class.extend(BaseAlanQweb,{
    xmlDependencies: [ '/theme_alan/static/src/xml/snippets/image_gallery_dialog.xml',
                       '/theme_alan/static/src/xml/snippets/base_templates.xml' ],
    events:{'click .set-img-gallery-config':'_image_gallery_configure' },
    init: function(){
        this._super.apply(this, arguments);
    },
    onBuilt: function(){
        this._super();
        this._image_gallery_configure();
    },
    _image_gallery_configure: function(){
        let cr = this;
        const imgData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_image_modal", {'type': 'Image'})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            tabData:cr.$target.attr("data-tabData"),
            popupType:"tabImage",
        }
        cr.brandCatDialog = new brandCatDialog(cr, imgData);
        cr.brandCatDialog.open();
    },
    cleanForSave: function(){
        this.$target.empty();
    },
});
});