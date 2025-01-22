odoo.define('theme_alan.common_modal', function (require) {
'use strict';

var Dialog = require('web.Dialog');

var common_modal = Dialog.extend({
	template: 'theme_alan.core_front_dialog',
	xmlDependencies: Dialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_front_dialog.xml']),
	events: _.extend({}, Dialog.prototype.events, {
        'click .as_close':'close',
    }),
    willStart:function(){
        return this._super.apply(this, arguments).then(() => {
            this.$modal.addClass("as-common-modal as-modal as-hotspot-static-modal").removeClass("o_technical_modal");
        });
    },
    init: function (src, opts) {
        let initData = {
                subTemplate: opts.subTemplate || "", renderHeader: 0, renderFooter: 0,
                size:opts.size || 'large', viewType: opts.viewType || false,  backdrop: true
            }
        this._super(src, _.extend(initData));
        this.options = opts;
    },
});
return common_modal

});