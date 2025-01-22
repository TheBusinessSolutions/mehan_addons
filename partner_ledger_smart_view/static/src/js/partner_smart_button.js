odoo.define('partner_ledger_smart_view.SmartPartnerLedger', function (require) {
    'use strict';
    var core = require('web.core');
    // var field_utils = require('web.field_utils');
    // var rpc = require('web.rpc');
    // var session = require('web.session');
    // var utils = require('web.utils');
    var QWeb = core.qweb;
    // var _t = core._t;


    // var datepicker = require('web.datepicker');
    // var time = require('web.time');

    // window.click_num = 0;
    var partner_ledger = require('dynamic_accounts_report.partner_ledger');
    

    var SmartPartnerLedger  = partner_ledger.extend({
        

    init: function(parent, action) {
            this._super(parent, action);
            this.active_id = action.context.active_id

        },

        load_data: function (initial_render = true) {
            var self = this;
                self.$(".categ").empty();
                try{
                    var self = this;
                    self._rpc({
                        model: 'account.partner.ledger',
                        method: 'view_report',
                        args: [[this.wizard_id],self.active_id],
                    }).then(function(datas) {
                        _.each(datas['report_lines'], function(rep_lines) {
                        rep_lines.debit = self.format_currency(datas['currency'],rep_lines.debit);
                        rep_lines.credit = self.format_currency(datas['currency'],rep_lines.credit);
                        rep_lines.balance = self.format_currency(datas['currency'],rep_lines.balance);
                    });
                    if (initial_render) {
                        self.$('.filter_view_tb').html(QWeb.render('PLFilterView', {
                            filter_data: datas['filters'],
                        }));
                        self.$el.find('.journals').select2({
                            placeholder: ' Journals...',
                        });

                        self.$el.find('.account').select2({
                            placeholder: ' Accounts...',
                        });
                        self.$el.find('.partners').select2({
                        placeholder: 'Partners...',
                        });
                        self.$el.find('.reconciled').select2({
                        placeholder: 'Reconciled status...',
                        });
                        self.$el.find('.type').select2({
                        placeholder: 'Account Type...',
                        });
                        self.$el.find('.category').select2({
                        placeholder: 'Partner Tag...',
                        });
                        self.$el.find('.acc').select2({
                        placeholder: 'Select Acc...',
                        });
                        self.$el.find('.target_move').select2({
                        placeholder: 'Target Move...',
                        });
                    }
                    var child=[];
                    self.$('.table_view_tb').html(QWeb.render('PLTable', {
                        report_lines : datas['report_lines'],
                        filter : datas['filters'],
                        currency : datas['currency'],
                        credit_total : datas['credit_total'],
                        debit_total : datas['debit_total'],
                        debit_balance : datas['debit_balance']
                    }));
                });

                }
                catch (el) {
                    window.location.href
                    }

        },
    });
    core.action_registry.add("smart_pl", SmartPartnerLedger);
    return SmartPartnerLedger;
});
