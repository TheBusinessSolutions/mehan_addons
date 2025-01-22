odoo.define('sh_backmate_theme_adv.todo_systray', function (require) {
	"use strict";

	var core = require('web.core');
	var Dialog = require('web.Dialog');
	var Widget = require('web.Widget');
	var rpc = require('web.rpc');
	var SystrayMenu = require('web.SystrayMenu');
	var session = require('web.session');
	var _t = core._t;
	var QWeb = core.qweb;
	// var UserMenu = require('web.UserMenu');
	// UserMenu.prototype.sequence = 2;

    var todo_widget = require('sh_backmate_theme_adv.todo_widget');



	var ToDoTemplate = Widget.extend({
		template: "ToDoTemplate",
		events: {
			'click #todo_icon': '_click_todo',
		},
		init: function () {
			this._super.apply(this, arguments);
			var self = this;
		},
        _click_todo: function (ev) {
			ev.preventDefault();
			
			if ($('.todo_layout').length) {
				if ($('.sh_theme_model').length) {
					$('.todo_layout').removeClass('sh_theme_model');
				} else{
					$('.todo_layout').addClass('sh_theme_model');
				}
			}else{
				this.body_container = new todo_widget();
				this.body_container.appendTo($('.o_web_client')).then(function () {
					$('.todo_layout').addClass('sh_theme_model');
				});
			}
          
        },
        
        
	});

	ToDoTemplate.prototype.sequence = 100;
	
	rpc.query({
		model: 'res.users',
		method: 'search_read',
		fields: ['sh_enable_todo_mode'],
		domain: [['id', '=', session.uid]]
	}, { async: false }).then(function (data) {
		if (data) {
			_.each(data, function (user) {
				if (user.sh_enable_todo_mode) {
					SystrayMenu.Items.push(ToDoTemplate);

				}
			});

		}
	});

	return {
		ToDoTemplate: ToDoTemplate,
	};
});
