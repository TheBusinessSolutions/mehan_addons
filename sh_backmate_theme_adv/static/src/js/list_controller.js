odoo.define('sh_backmate_theme_adv.ListController', function (require) {
    "use strict";
    const rpc = require("web.rpc");
    var show_expand_collapse = false
    var session = require('web.session');

    rpc.query({
        model: 'res.users',
        method: 'search_read',
        fields: ['sh_enable_expand_collapse'],
        domain: [['id', '=', session.uid]]
    }, { async: false }).then(function (data) {
        if (data) {
            _.each(data, function (user) {
                if (user.sh_enable_expand_collapse) {
                    show_expand_collapse = true
                }
            });

        }
    });
    var ListController = require('web.ListController');

    ListController.include({
        init: function (parent, model, renderer, params) {
			this._super.apply(this, arguments);
            this.show_expand_collapse = show_expand_collapse
		 },
        events: _.extend({}, ListController.prototype.events, {
            'click .sh_refresh': '_onClickRefreshView',
            'click .sh_expand': 'shExpandGroups',
            'click .sh_collapse': 'shCollapseGroups',
        }),
        _onClickRefreshView:function (ev) {
           console.log("Refresh")
           this.reload()
        },
        shExpandGroups () {

            $(document).find('.o_group_header').each(function () {
                var $header = $(this);
                if (!$header.hasClass('o_group_open')) {
                    $header.find('.o_group_name').click();
                }
            });
        },
    
        shCollapseGroups () {
            $(document).find('.o_group_header').each(function () {
                var $header = $(this);
                if ($header.hasClass('o_group_open')) {
                    $header.find('.o_group_name').click();
                }
            });
        },
    });

    var ListRenderer = require('web.ListRenderer');

	ListRenderer.include({
		async _renderView() {
			// Fix issue of sticky three dots
			var self = this;
			return this._super.apply(this, arguments).then(function () {
				self.$el.find('thead').append(
								$('<i class="o_optional_columns_dropdown_toggle fa fa-ellipsis-v"/>')
							);
			});


		}
		    
	});

    
});
odoo.define('sh_backmate_theme_adv.BasicController', function (require) {
    "use strict";

    var BasicController = require('web.BasicController');

    BasicController.include({
        events: _.extend({}, BasicController.prototype.events, {
            'click .sh_refresh': '_onClickRefreshView',
        }),
        _onClickRefreshView:function (ev) {
           console.log("Refresh")
           this.reload()
        }
    });
});