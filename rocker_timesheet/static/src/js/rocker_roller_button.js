odoo.define('rocker_timesheet.rollerbutton', function(require) {
    'use strict';

    var core = require('web.core');
    var viewRegistry = require('web.view_registry');
    var ListController = require('web.ListController');
    var ListView = require("web.ListView");

    var _t = core._t;
    var QWeb = core.qweb;


    var RockerListController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .btn-roller': '_onCreateRolling',
        }),
        start: function () {
            this.$el.addClass('o_rocker_roller_tree');
            return this._super(...arguments);
        },

         //--------------------------------------------------
         // Buttons
         //--------------------------------------------------

        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            $(QWeb.render('rocker_timesheet.roller-button', {
                roller: _t('Rolling'),
            })).appendTo(this.$buttons);

            this.$buttons.appendTo($node);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        _onCreateRolling: async function () {
            var self = this;
            await this.do_action('rocker_timesheet.action_create_rolling', {
                on_close: function () {
//                    self.reload();
                }
            });
            $(this.$buttons).find('.o_list_button_add').click();
        },

    });

    var RockerListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: RockerListController,
        }),
    });


    viewRegistry.add('rocker_roller_tree', RockerListView);


});
