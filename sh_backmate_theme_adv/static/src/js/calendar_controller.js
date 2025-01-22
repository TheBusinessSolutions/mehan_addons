odoo.define('sh_backmate_theme_adv.CalendarController', function (require) {
    "use strict";

    var CalendarController = require('web.CalendarController');

    CalendarController.include({
        events: _.extend({}, CalendarController.prototype.events, {
            'click .sh_refresh': '_onClickRefreshView',
        }),
        _onClickRefreshView:function (ev) {
           console.log("Refresh")
           this.reload()
        }
    });
});