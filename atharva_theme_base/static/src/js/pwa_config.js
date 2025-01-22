odoo.define('atharva_theme_base.pwa_config', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.pwa = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    start: function() {
        // PWA initialization
        this._super.apply(this, arguments);
        if(this.$target.data("pwa") == 1){
            if('serviceWorker' in navigator){
                navigator.serviceWorker.register('/service-worker-js')
            }
        }
        else{
            if(navigator.serviceWorker) {
                navigator.serviceWorker.getRegistrations().then(function(reg) {
                    _.each(reg, function(sw) {
                        sw.unregister();
                    });
                });
            }
        }
    },
});
});