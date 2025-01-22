odoo.define('atharva_theme_base.lazy_loader', function (require) {
'use strict';

const publicWidget = require('web.public.widget');

var aslazyLoader = publicWidget.Widget.extend({
    disabledInEditableMode: false,
    willStart: function () {
        var cr = this;
        var parent = cr._super.bind(cr, ...arguments);
        if(!cr.editableMode){
            var _itsTimeToShow = function () {
                var show = new Promise((success, fail) => {
                    var cur_target = $('#wrapwrap');
                    var pos = cur_target.scrollTop();
                    var scroll_pos = cur_target.scrollTop();
                    if (scroll_pos == pos) {
                        var cur_data = document.documentElement.clientHeight ||
                            window.innerHeight || document.body.clientHeight;
                        if((cr.$target.offset().top - cur_data) < 100){
                            success();
                        }
                    }
                    pos = scroll_pos;
                    cur_target.on('scroll', _.throttle((ev) => {
                        var scroll_pos = cur_target.scrollTop();
                        if (scroll_pos > pos) {
                            var cur_data = document.documentElement.clientHeight ||
                                window.innerHeight || document.body.clientHeight;
                            if((cr.$target.offset().top - cur_data) < 100){
                                success();
                            }
                        }
                        pos = scroll_pos;
                    }, 300));
                });
                return show;
            }
            if (cr.$target.hasClass('as-load')) {
                return _itsTimeToShow().then(() => {return parent()});
            }else{
                return parent();
            }
        }
        return parent();
    },
})
return aslazyLoader
})