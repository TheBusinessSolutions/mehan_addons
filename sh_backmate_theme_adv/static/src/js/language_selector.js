
// ===========================================
//	Language list
// ===========================================

odoo.define('sh_backmate_theme_adv.language_selector_list', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var SystrayMenu = require('web.SystrayMenu');
    var _t = core._t;
    var QWeb = core.qweb;
    var session = require('web.session');

    var language_list = Widget.extend({
        template: "LanguageTemplate",
        events: {
            'click a.sh_user_lang': 'change_sh_user_lang',
        },
        change_sh_user_lang: function(e){
            var self = this;
            var lang = $(e.currentTarget).data('language');
            var self = this;
        	self._rpc({
				model: "res.users",
				method: "write",
				args: [parseInt(session.user_context.uid), {
					'lang': lang,
				}],
			}).then(function (data) {
                self.do_action("reload_context");
            });
            
        },
        init: function () {
            this._super.apply(this, arguments);

        },
        start: function () {
            var self = this;
            rpc.query({
                model: 'res.lang',
                method: 'sh_get_installed_lang',
            }).then(function (languages) {
                self.$el.find('.sh_user_language_list_cls').html(QWeb.render("LanguageTemplate.list", { languages_list: languages, selected_lang : session.user_context.lang }));
            });

            return this._super();
        },

    });
    language_list.prototype.sequence = 4;
   
    rpc.query({
		model: 'res.users',
		method: 'search_read',
		fields: ['sh_enable_language_selection'],
		domain: [['id', '=', session.uid]]
	}, { async: false }).then(function (data) {
		if (data) {
			_.each(data, function (user) {
				if (user.sh_enable_language_selection) {
					SystrayMenu.Items.push(language_list);

				}
			});

		}
	});

    return {
        language_list: language_list,
    };
});

