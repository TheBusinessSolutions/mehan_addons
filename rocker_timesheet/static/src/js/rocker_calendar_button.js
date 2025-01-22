odoo.define('rocker_timesheet.calendar-button', function(require) {
    'use strict';

    var rpc = require('web.rpc');
    var core = require('web.core');
    var session = require('web.session');
    var CalendarPopover = require('web.CalendarPopover');
    var CalendarController = require("web.CalendarController");
    var CalendarRenderer = require("web.CalendarRenderer");
    var CalendarView = require("web.CalendarView");
    var CalendarModel = require('web.CalendarModel');
    var AbstractRenderer = require('web.AbstractRenderer');
    var viewRegistry = require('web.view_registry');

    var _t = core._t;
    var QWeb = core.qweb;

    var minTime = '00:00:00';
    var maxTime = '24:00:00';
    var slot = "30";
    var defaultMode = 'month';
    var defaultModeSet = false;

    String.prototype.toHHMMSS = function () {
        var hour_num = parseFloat(this);
        var hours   = Math.trunc(hour_num);
        var minutes = (hour_num - hours) * 60;
        if (hours   < 10) {hours   = "0"+hours;}
        if (minutes < 10) {minutes = "0"+minutes;}
        return hours+':'+minutes+':'+'00';
    }

    async function get_rocker_defaults() {
//                   console.log('function get_rocker_user_defaults');
                   var model = 'rocker.user.defaults';
                    var uid = session.uid;
                    var cid = session.user_context.allowed_company_ids[0];
                   var res = rpc.query({
                      model: model,
                      method: 'get_rocker_user_defaults',
                      args: [uid, cid],
                       }).then(function (data) {
//                        console.log(data);
                        if (data[0] > 0) {
//                            console.log('Found User Defaults');
                            minTime = String(parseInt(data[2])).toHHMMSS();
                            maxTime = String(parseInt(data[3])).toHHMMSS();
                            slot = String(parseInt(data[4])/60).toHHMMSS();
                            defaultMode = data[5];
                            return true;
                            }
                            console.log('No User Defaults, creating defs');
                           minTime = String(0).toHHMMSS();
                           maxTime = String(24).toHHMMSS();
                           slot = String(1).toHHMMSS();
                           defaultMode = "month";
                           return true;

                        });

    }


    var RockerCalendarController = CalendarController.extend({
        events: _.extend({}, CalendarController.prototype.events, {
            'click .btn-all': '_onAll',
            'click .btn-billable': '_onBillable',
            'click .btn-nonbillable': '_onNonBillable',
            'click .btn-internal': '_onInternal',
            'click .btn-member': '_onMember',
            'click .btn-mine': '_onMine',
        }),

        start: function () {
            this.$el.addClass('o_rocker_calendar');
            return this._super(...arguments);
        },


         //--------------------------------------------------
         // Buttons
         //--------------------------------------------------

        renderButtons: function ($node) {
            this._super.apply(this, arguments);
            $(QWeb.render('rocker_timesheet.calendar-button', {
                all: _t('All'),
                billable: _t('Billable'),
                nonbillable: _t('NonBillable'),
                internal: _t('Internal'),
                member: _t('Member'),
                mine: _t('My'),
            })).appendTo(this.$buttons);

            this.$buttons.appendTo($node);
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        _onAll: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_all_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onMember: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_member_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onBillable: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_billable_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onNonBillable: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_nonbillable_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onInternal: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_internal_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },
        _onMine: function () {
            var self = this;
            this.do_action('rocker_timesheet.action_searchpanel_mine_tasks', {
                on_close: function () {
//                    self.reload();
                }
            });
        },

    });

    var RockerCalendarModel = CalendarModel.include({

//        init: function () {
//            this._super.apply(this, arguments);
//            console.log('Rocker model init');
//        },

        _loadCalendar: function () {
//            console.log('_loadCalendar');
            var result = this._super.apply(this, arguments);
            var res = get_rocker_defaults();
//               console.log(this);
//               console.log(minTime);
//               console.log(maxTime);
//               console.log(slot);
//               console.log(defaultMode);
//               console.log('defaultMode:');
//               console.log(defaultMode);
//               this.setScale('day');
                if (defaultModeSet == false) {
                    this.setScale(defaultMode)
                    defaultModeSet = true;
                    }
            return result;
            },

        _getFullCalendarOptions: function () {
//            console.log('_getFullCalendarOptions');
            var res = get_rocker_defaults();
//            console.log('minTime, maxTime, slot');
//            console.log(minTime);
//            console.log(maxTime);
//            console.log(slot);
//            console.log(defaultMode);
            var result = this._super.apply(this, arguments);
//            console.log(result);
            result.slotDuration =
                this.data.context.calendar_slot_duration ||
                result.slotDuration ||
                slot;
            result.minTime =
                this.data.context.minTime ||
                result.minTime ||
                minTime;
            result.maxTime =
                this.data.context.maxTime ||
                result.maxTime ||
                maxTime;
//            console.log(result);
            return result;
        },   // _fullCalendarOptions
    });  // RockerCalendarModel

    var RockerCalendarView = CalendarView.extend({
        config: _.extend({}, CalendarView.prototype.config, {
//            CalendarRenderer: RockerCalendarRenderer,
            Controller: RockerCalendarController,
            CalendarModel: RockerCalendarModel,
       }),

           init: function (viewInfo, params) {
                console.log('Rocker view init');
                var self = this;
                this._super.apply(this, arguments);
                var res = get_rocker_defaults();
                defaultModeSet = false;   // change view mode only once
//                console.log(this);
//            console.log(minTime);
//            console.log(maxTime);
//            console.log(slot);
//            console.log(defaultMode);
            },
    });

    viewRegistry.add('rocker_calendar', RockerCalendarView);

    return RockerCalendarView


});
