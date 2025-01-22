//===========================================
//toggle switch if quick menu already exists
//===========================================

// odoo.define('sh_web_quick_menu.quick_menu_already', function (require) {
//     "use strict";

//     var core = require('web.core');
//     var Dialog = require('web.Dialog');
//     var Widget = require('web.Widget');
//     var rpc = require('web.rpc');
//     var SystrayMenu = require('web.SystrayMenu');
//     var menu = require('web.Menu');
//     var ActionManager = require('web.ActionManager');
//     var _t = core._t;
//     var QWeb = core.qweb;

//     var ActionManager = ActionManager.include({

//         _preprocessAction: function (action, options) {
//             var self = this;
//             this._super.apply(this, arguments);

//             if (action && action.id) {
//                 rpc.query({
//                     model: 'sh.wqm.quick.menu',
//                     method: 'is_quick_menu_avail',
//                     args: ['', action.id]
//                 }).then(function (rec) {
//                     if (rec) {
//                         $('.o_user_bookmark_menu > a').addClass('active');

//                     }
//                     else {
//                         $('.o_user_bookmark_menu > a').removeClass('active');
//                     }
//                 });
//             }

//         },

//     });


//     var menu = menu.include({

//         getMenuRecord: function (menu_id) {
//             return rpc.query({
//                 model: 'sh.wqm.quick.menu',
//                 method: 'is_already_have_in_quick_menu',
//                 args: ['', menu_id]
//             });
//         },

//         _trigger_menu_clicked: function (menu_id, action_id) {
//             var self = this;
//             this._super.apply(this, arguments);

//             this.getMenuRecord(menu_id).then(function (rec) {

//                 if (rec) {
//                     self.$el.find('.o_user_bookmark_menu > a').addClass('active');
//                 } else {
//                     self.$el.find('.o_user_bookmark_menu > a').removeClass('active');
//                 }
//             });

//         },

//     });


//     //return menu;
//     //return {
//     //  quick_menu: quick_menu,
//     //};
// });



//===========================================
//Quick Menu (main on off switch)
//===========================================

odoo.define('sh_web_quick_menu.quick_menu', function (require) {
    "use strict";

    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var Widget = require('web.Widget');
    var rpc = require('web.rpc');
    var SystrayMenu = require('web.SystrayMenu');
    var session = require('web.session');
    var _t = core._t;
    var QWeb = core.qweb;


    var quick_menu = Widget.extend({
        template: "quick.menu",
        events: {
            dblclick: "on_click",
            'click li.sh_wqm_remove_quick_menu_cls i': 'remove_quick_menu',
            "keydown input.sh_bookmark_search": "_onSearchResultsNavigate",
        },
        _searchData: function () {
            var query = this.$("input.sh_bookmark_search").val();
          
            var self = this;
            var quick_menus_var = rpc.query({
                model: 'sh.wqm.quick.menu',
                method: 'get_search_result',
                args: [[query]]
            })
                .then(function (menus) {

                    if (menus.length > 0) {
                        self.$el.find('.sh_search_result').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': menus}));
                    } else {
                        self.$el.find('.sh_search_result').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }
                });
            
        },

        _onSearchResultsNavigate: function (event) {

            this._search_def.reject();
            this._search_def = $.Deferred();
            setTimeout(this._search_def.resolve.bind(this._search_def), 50);
            this._search_def.done(this._searchData.bind(this));
        },


        init: function () {
            this._search_def = $.Deferred();
            this._super.apply(this, arguments);

        },
        remove_quick_menu: function (e) {
            e.stopPropagation();
            var self = this;
            var id = parseInt($(e.currentTarget).data('id'));
            if (id !== NaN) {
                rpc.query({
                    model: 'sh.wqm.quick.menu',
                    method: 'remove_quick_menu_data',
                    args: ['', id]
                }).then(function (res) {
                    if (res.id) {
                        if (window.location.href == res.sh_url) {
                            self.$el.parents().find('.sh_bookmark').removeClass('active');
                        }
                        
                        if (res.final_quick_menu_list.length > 0) {
                            if(res.final_quick_menu_list.length > 13){
                                self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': res.final_quick_menu_list }));
                            }else{
                                self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': res.final_quick_menu_list }));
                      
                            }

                        } else {
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                        }
                    }
                });
            }
            return false;
        },
        getUrlVars: function () {
            var vars = [], hash;
            var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
            for (var i = 0; i < hashes.length; i++) {
                hash = hashes[i].split('=');
                vars.push(hash[0]);
                vars[hash[0]] = hash[1];
            }
            return vars;
        },
        getUrl: function () {

            return window.location.href;
        },

        start: function () {
            //this.$var = this.$el.find('.sh_wqm_quick_menu_submenu_list_cls');
            var self = this;
            var quick_menus_var = rpc.query({
                model: 'sh.wqm.quick.menu',
                method: 'get_quick_menu_data',
                args: ['', ['name', 'sh_url']],
            })
                .then(function (menus) {

                    if (menus.length > 0) {
                        if(menus.length > 13){
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': menus }));
                        }else{
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': menus }));
                  
                        }
                    } else {
                        self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }
                });
            return this._super();

            //return this._super();
        },
        getMenuRecord: function () {
            var action_id = $.bbq.getState().action;

            var model = $.bbq.getState().model
            if(!$.bbq.getState().model){
                model = $.bbq.getState().active_id
            }
            if ($.bbq.getState().view_type == 'form') {
                var res_id = $.bbq.getState().id
            }
            var sh_url = this.getUrl()
            return rpc.query({
                model: 'sh.wqm.quick.menu',
                method: 'set_quick_url',
                args: ['', sh_url, model, res_id, action_id]
            });
        },
        on_click: function (ev) {
            ev.preventDefault();
            ev.stopPropagation();
            var self = this;
            this.getMenuRecord().then(function (rec) {
                self.$el.addClass('active');
                if (rec.is_set_quick_menu) {
                    if (rec.final_quick_menu_list.length > 0) {

                        if(rec.final_quick_menu_list.length > 13){
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                        }else{
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                  
                        }


                    } else {
                        self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }

                    
                } else {
                    self.$el.removeClass('active')
                    if (rec.final_quick_menu_list.length > 0) {
                        if(rec.final_quick_menu_list.length > 13){
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                        }else{
                            self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'quick_menulist_actions': rec.final_quick_menu_list }));
                  
                        }

                    } else {
                        self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist", { 'no_menu': 1 }));
                    }
                }
            });
            //refresh the page
            //location.reload(true);

        }
    });

    quick_menu.prototype.sequence = 3;
    // session.user_has_group('sh_backmate_theme_adv.group_quick_menu_mode').then(function (has_group) {
    //     if (has_group) {
    //         SystrayMenu.Items.push(quick_menu);
    //     }
    // });
    rpc.query({
		model: 'res.users',
		method: 'search_read',
		fields: ['sh_enable_quick_menu_mode'],
		domain: [['id', '=', session.uid]]
	}, { async: false }).then(function (data) {
		if (data) {
			_.each(data, function (user) {
				if (user.sh_enable_quick_menu_mode) {
					SystrayMenu.Items.push(quick_menu);

				}
			});

		}
	});


    //return quick_menu;
    return {
        quick_menu: quick_menu,
    };
});




// ===========================================
//	Quick Menu List
// ===========================================

// odoo.define('sh_web_quick_menu.quick_menulist', function (require) {
//     "use strict";

//     var core = require('web.core');
//     var Dialog = require('web.Dialog');
//     var Widget = require('web.Widget');
//     var rpc = require('web.rpc');
//     var SystrayMenu = require('web.SystrayMenu');
//     var _t = core._t;
//     var QWeb = core.qweb;
//     var session = require('web.session');
//     var quick_menulist = Widget.extend({
//         template: "quick.menulist",

//         events: {
//             'click li.sh_wqm_remove_quick_menu_cls i': 'remove_quick_menu',
//         },

//         remove_quick_menu: function (e) {
//             e.stopPropagation();
//             var self = this;
//             var id = parseInt($(e.currentTarget).data('id'));
//             if (id !== NaN) {
//                 rpc.query({
//                     model: 'sh.wqm.quick.menu',
//                     method: 'remove_quick_menu_data',
//                     args: ['', id]
//                 }).then(function (res) {
//                     if (res.id) {
//                         if ($.bbq.getState(true).action == res.action_id) {
//                             self.$el.parents().find('.o_user_bookmark_menu > a').removeClass('active');
//                         }

//                         //refresh by the base url at remove time.
//                         var base_url = window.location.origin;
//                         window.location = base_url + "/web";
//                         //                        location.reload(true);

//                     }
//                 });
//             }
//             return false;
//         },

//         init: function () {
//             this._super.apply(this, arguments);

//         },
//         start: function () {
//             //this.$var = this.$el.find('.sh_wqm_quick_menu_submenu_list_cls');
//             var self = this;
//             var quick_menus_var = rpc.query({
//                 model: 'sh.wqm.quick.menu',
//                 method: 'get_quick_menu_data',
//                 args: ['', ['name', 'sh_url']],
//             })
//                 .then(function (menus) {

//                     if (menus.length > 0) {
//                         self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'quick_menulist_actions': menus }));
//                     } else {
//                         self.$el.find('.sh_wqm_quick_menu_submenu_list_cls').html(QWeb.render("quick.menulist.actions", { 'no_menu': 1 }));
//                     }
//                 });
//             return this._super();
//         },
//     });
//     quick_menulist.prototype.sequence = 4;
//     // session.user_has_group('sh_backmate_theme_adv.group_quick_menu_mode').then(function (has_group) {
//     //     if (has_group) {
//     //         SystrayMenu.Items.push(quick_menulist);
//     //     }
//     // });

//     rpc.query({
// 		model: 'res.users',
// 		method: 'search_read',
// 		fields: ['sh_enable_quick_menu_mode'],
// 		domain: [['id', '=', session.uid]]
// 	}, { async: false }).then(function (data) {
// 		if (data) {
// 			_.each(data, function (user) {
// 				if (user.sh_enable_quick_menu_mode) {
// 					SystrayMenu.Items.push(quick_menulist);

// 				}
// 			});

// 		}
// 	});

//     //return quick_menu;
//     return {
//         quick_menulist: quick_menulist,
//     };
// });

