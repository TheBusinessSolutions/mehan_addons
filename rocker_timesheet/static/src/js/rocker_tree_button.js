odoo.define('rocker_timesheet.tree-button', function(require) {
    'use strict';

    var core = require('web.core');
    var CalendarPopover = require('web.CalendarPopover');
    var CalendarController = require("web.CalendarController");
    var CalendarRenderer = require("web.CalendarRenderer");
    var CalendarView = require("web.CalendarView");
    var viewRegistry = require('web.view_registry');
    var ListController = require('web.ListController');
    var ListView = require("web.ListView");

    var _t = core._t;
    var QWeb = core.qweb;



    var RockerListController = ListController.extend({
        events: _.extend({}, ListController.prototype.events, {
            'click .btn-all2': '_onAll2',
            'click .btn-billable2': '_onBillable2',
            'click .btn-nonbillable2': '_onNonBillable2',
            'click .btn-internal2': '_onInternal2',
            'click .btn-member2': '_onMember2',
            'click .btn-mine2': '_onMine2',
            'click .btn-roller2': '_onCreateRolling2',
        }),
        start: function () {
            this.$el.addClass('o_rocker_tree');
            return this._super(...arguments);
        },

         //--------------------------------------------------
         // Buttons
         //--------------------------------------------------

        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            $(QWeb.render('rocker_timesheet.tree-button', {
                all2: _t('All'),
                billable2: _t('Billable'),
                nonbillable2: _t('NonBillable'),
                internal2: _t('Internal'),
                member2: _t('Member'),
                mine2: _t('My'),
                roller2: _t('Rolling'),
            })).appendTo(this.$buttons);

            this.$buttons.appendTo($node);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        _onAll2: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_all_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onMember2: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_member_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onBillable2: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_billable_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onNonBillable2: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_nonbillable_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onInternal2: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_internal_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onMine2: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_mine_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onCreateRolling2: async function () {
            var self = this;
            await this.do_action('rocker_timesheet.action_create_rolling', {
                on_close: function () {
//                    self.reload();
                }
            });
//            console.log('Wait');
//            await;
            $(this.$buttons).find('.o_list_button_add').click();
        },

    });

    var RockerListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: RockerListController,
        }),
    });


    viewRegistry.add('rocker_tree', RockerListView);


});
