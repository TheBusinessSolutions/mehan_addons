odoo.define('sh_backmate_theme_adv.todo_widget', function (require) {
	"use strict";

	var ajax = require('web.ajax');
	var core = require('web.core');
	var Widget = require('web.Widget');
	var QWeb = core.qweb;
	var rpc = require("web.rpc");
	const session = require("web.session");
	ajax.loadXML('/sh_backmate_theme_adv/static/src/xml/todo.xml', core.qweb)
	
	var ToDoWidget = Widget.extend({
		template: 'ToDoWidget',
		events: {
            'click .close_todo_setting' : '_close_todo',
			'click .sh_add_todo': '_click_add_todo',
			'change .sh_todo_checklist':'_click_sh_todo_checklist',
			'click .sh_header_pencil':'_click_sh_header_pencil',
			'click .sh_header_save':'_focusout_sh_todo_description',
			'click .sh_header_times':'_remove_todo',
			'keydown .sh_add_todo_input': '_onKeydown',
		},
		willStart: function () {
			var self = this;
			
	        return this._super.apply(this, arguments).then(function () {

				var accordion_html = ''
				self.getAllTodo().then(function (each_data) {
					_.each(each_data, function (todo_data) {
						accordion_html += QWeb.render("ToDoCard", {
							name: todo_data.name,
							rec:parseInt(todo_data.id),
							is_done:todo_data.is_done,
							widget: self,
						})
						
					});
					$("#accordion").html(accordion_html);
					$('#accordion').sortable({
						stop: function(event, ui) {

							var itemOrder = $('#accordion').sortable("toArray");
							for (var i = 0; i < itemOrder.length; i++) {
							  rpc.query({
									model: 'sh.todo',
									method: 'write',
									args: [[ itemOrder[i]], {
										sequence: i+10,
									}],
								});

							  
							}
					  
						  }
					});
				});
				

	        })
	    },

		start: function () { 
			var self = this;
			var accordion_html = ''
				self.getAllTodo().then(function (each_data) {
					_.each(each_data, function (todo_data) {
						accordion_html += QWeb.render("ToDoCard", {
							name: todo_data.name,
							rec:parseInt(todo_data.id),
							is_done:todo_data.is_done,
							widget: self,
						})
						
					});
					$("#accordion").html(accordion_html);
				});
			return this._super();
		},
		_onKeydown: function (ev) {
			ev.stopPropagation();
			if (ev.which === 13) {

				var self = this;
				var todo_input = $(".sh_add_todo_input").val()
				if(!$(".sh_add_todo_input").val()){
					alert("Please Enter Title !")
				}else{
					ev.stopPropagation();
					this.saveTodo(todo_input).then(function (rec) {
						$("#accordion").prepend(QWeb.render("ToDoCard", {
							name: todo_input,
							rec:parseInt(rec),
							widget: self,
						}));
					});
		
					$(".sh_add_todo_input").val("")
			}
				
			}
		},
		_click_sh_header_pencil: function (ev) {
			ev.preventDefault();
			$(ev.currentTarget).parents('.card').find('.sh_todo_description').css("display","block");
			$(ev.currentTarget).parents('.card').find('.sh_todo_label').css("display","none");
			$(ev.currentTarget).parents('.card').find('.sh_header_pencil').css("display","none");
			$(ev.currentTarget).parents('.card').find('.sh_header_save').css("display","block");
			var fieldInput = $(ev.currentTarget).parents('.card').find('.sh_todo_description');
			// fieldInput.removeAttr("readonly")
			var fldLength= fieldInput.val().length;
			fieldInput.focus();
			fieldInput[0].setSelectionRange(fldLength, fldLength);
			// fieldInput.addClass("sh_edit_todo_lable")



		},
		
		_focusout_sh_todo_description: function (ev) {
			ev.preventDefault();
			var fieldInput = $(ev.currentTarget).parents('.card').find('.sh_todo_description');
			$(ev.currentTarget).parents('.card').find('.sh_header_pencil').css("display","block");
			$(ev.currentTarget).parents('.card').find('.sh_header_save').css("display","none");
			fieldInput.css("display","none");
			$(ev.currentTarget).parents('.card').find('.sh_todo_label').css("display","block");
			$(ev.currentTarget).parents('.card').find('.sh_todo_label').text(fieldInput.val())
			var todo_id  = $(ev.currentTarget).attr('id')
			rpc.query({
                model: 'sh.todo',
                method: 'write',
                args: [[todo_id], {
                    name: fieldInput.val(),
                }],
            });

		},
		_remove_todo: function (ev) {
			ev.preventDefault();
			var self = this;
			var todo_id  = $(ev.currentTarget).attr('id')
			this.removeTodo(todo_id).then(function (data) {
				var accordion_html = ''
				self.getAllTodo().then(function (each_data) {
					_.each(each_data, function (todo_data) {
						accordion_html += QWeb.render("ToDoCard", {
							name: todo_data.name,
							rec:parseInt(todo_data.id),
							is_done:todo_data.is_done,
							widget: self,
						})
						
					});
					$("#accordion").html(accordion_html);
				});
            });
		},
		removeTodo: function ( todo_id) {
			return rpc.query({
                model: 'sh.todo',
                method: 'unlink',
                args: [todo_id],
            });

            
        },
		_close_todo: function (ev) {
			ev.preventDefault();
            $('.todo_layout').removeClass('sh_theme_model');
        },
		saveTodo: function (todo_input) {
            return rpc.query({
                model: 'sh.todo',
                method: 'create',
                args: [{name: todo_input}],
            });
        },

		_click_add_todo: function (ev) {
			ev.preventDefault();
			var self = this;
			var todo_input = $(".sh_add_todo_input").val()
			if(!$(".sh_add_todo_input").val()){
				alert("Please Enter Title !")
			}else{
				ev.stopPropagation();
				this.saveTodo(todo_input).then(function (rec) {
					$("#accordion").prepend(QWeb.render("ToDoCard", {
						name: todo_input,
						rec:parseInt(rec),
						widget: self,
					}));
				});
	
				$(".sh_add_todo_input").val("")
			}
			
			

        },
		doneTodo: function (done_todo ,todo_id) {
			return rpc.query({
                model: 'sh.todo',
                method: 'write',
                args: [[todo_id], {
                    is_done: done_todo,
                }],
            });

            
        },
		getAllTodo: function () {
			return rpc.query({
                model: 'sh.todo',
                method: 'search_read',
				fields: ['name','is_done'],
				domain: [['user_id', '=', session.uid]],
            });

            
        },
		_click_sh_todo_checklist: function (ev) {
			
			ev.preventDefault();
			var self = this;
			var done_todo = $(ev.currentTarget).prop("checked")
			var todo_id  = $(ev.currentTarget).attr('id').split('todo-checkbox-')[1]
			this.doneTodo(done_todo, todo_id).then(function (data) {
				var accordion_html = ''
				self.getAllTodo().then(function (each_data) {
					_.each(each_data, function (todo_data) {
						accordion_html += QWeb.render("ToDoCard", {
							name: todo_data.name,
							rec:parseInt(todo_data.id),
							is_done:todo_data.is_done,
							widget: self,
						})
						
					});
					$("#accordion").html(accordion_html);
				});
				
				
				
                
            });
		}
	});
	return ToDoWidget;
});;