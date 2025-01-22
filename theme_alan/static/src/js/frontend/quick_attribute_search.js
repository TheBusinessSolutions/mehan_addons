odoo.define('theme_alan.quick_attribute_search', function (require) {
'use strict';

var WebsiteSale = require('website_sale.website_sale');
var publicWidget = require('web.public.widget');
var webCore = require('web.core');
const webUtils = require('web.utils');
var _t = webCore._t;
var quick_dialog = require('theme_alan.quick_modal');
const { AlanTemplateGetter } = require("theme_alan.core_mixins");

publicWidget.registry.WebsiteSale.include({

    _onChangeAttribute: function (ev) {
        if (!ev.isDefaultPrevented()) {
            ev.preventDefault();
            if(!$(ev.currentTarget).hasClass('as-attr-search')){
                if(!$(ev.currentTarget).hasClass('as-brands-search')){
                    $(ev.currentTarget).closest("form").submit();
                }
            }
        }
    },
});

publicWidget.registry.qckEleSrchPopup = publicWidget.Widget.extend({
    selector: '.as-shop',
    xmlDependencies: ['/atharva_theme_base/static/src/xml/quick_search_modal.xml'],
    events: {'click .quick_modal': '_quickPopup',
             'click .quick_attr_list': '_quicklist'},

    _quicklist: function(ev) {
        var selAttrib = $(ev.currentTarget).attr("data-title");
        $('.shop-attribs-'+selAttrib).removeClass('as-d-none');
        $('.extra-'+selAttrib).addClass('as-d-none');
    },

    _quickPopup: function(ev) {
        var self = this;
        var title = $(ev.currentTarget).attr('data-title');
        var dataType = $(ev.currentTarget).attr('data-dataType');
        var counter = $(ev.currentTarget).attr('data-counter');
        var no_prod = $(ev.currentTarget).attr('no-prod');
        var prod_count = JSON.parse($(ev.currentTarget).attr('prod-counter').replace(/'/g,'"'));
        var alphabets = Object.values(JSON.parse($(ev.currentTarget).attr('data-alphabets').replace(/'/g,'"')));
        var dataList = $(ev.currentTarget).attr('data-list').replace(/'/g,'"');
        return this._rpc({
            route: '/get/quick_modal_data_ids',
            params: {'dataList': dataList, 'dataType': dataType},
        }).then(function(res){
            var selData = $(ev.currentTarget).attr('data-selData');
            if (no_prod != undefined){
                no_prod = 'false';
            }
            if (selData != undefined){
                selData = JSON.parse($(ev.currentTarget).attr('data-selData').replace(/'/g,'"'));
            }
            return self._rpc({
                route: '/get/quick_modal_data',
                params: {'alphabets': alphabets, 'dataType': dataType, 'dataList': res['modal_data_list'], 'counter': counter, 'prod_count': prod_count, 'no_prod': no_prod, 'selData': selData, 'curr_alpha': res['curr_alpha']}
            }).then(function (response) {
                var quickDialog = new quick_dialog(this,{
                    subTemplate:webUtils.Markup(response['template']),
                    size:'large',
                    viewType:'quick-search',
                });
                quickDialog.open();
            });
        });
    },
});

publicWidget.registry.quickAttribSearch = publicWidget.Widget.extend(AlanTemplateGetter,{
    selector: '.as-qck-attr-src',
    events: {'input .as-attr-search': "_asAttrChange",
             'input .as-categ-search': "_asCategChange", },

    _quickSearchAttr:function(attr_vals, attr_name, vals, total_ele){
        var i = 0;
        $.each(attr_vals, function (ind, val) {
            var name = $(val).attr(attr_name);
            name = name.toLowerCase();
            vals = vals.toLowerCase();
            var all = $(val).parents().closest('li').find('.extra-eles').hasClass('as-d-none');
            if (vals == ""){
                if ($(val).parent().attr('data-default-show') == "true"){
                    $(val).parent().removeClass('as-d-none as');

                } else {
                    if (all == false){
                        $(val).parent().addClass('as-d-none as');
                    } else {
                        $(val).parent().removeClass('as-d-none as');
                    }
                }
            } else {
                if (name.includes(vals)){
                    i++;
                    $(val).parent().removeClass('as-d-none as');
                    if (i == total_ele){
                        i = 0;
                        return false;
                    }
                } else {
                    $(val).parent().addClass('as-d-none as');
                }
            }
        });
        var no_attrib = this.$target.parents().closest('li').find('.as').length;
        if (no_attrib == attr_vals.length){
            this.$target.children('.no_match_attrib').removeClass('as-d-none');
            this.$target.parents().closest('li').find('.extra-eles').addClass('as-disabled');
        } else {
            this.$target.children('.no_match_attrib').addClass('as-d-none');
            this.$target.parents().closest('li').find('.extra-eles').removeClass('as-disabled');
        }
    },
    _asAttrChange: function(ev){
        ev.preventDefault();
        var value = this.$target.find(".as-attr-search").val();
        var total_ele = this.$target.find(".as-attr-search").attr('data-total-ele');
        var brands = this.$target.parents().closest(".nav-item").find(".shop_brands").find("input[name='brand']");
        var qck_attr = this.$target.parents().closest(".nav-item").find(".as_shop_attribs").find("input[name='attrib']");
        var tags = this.$target.parents().closest(".nav-item").find('.shop_tags').find("input[name='tag']");
        if(brands.length != 0){
            this.$target.parents().closest(".nav-item").find(".shop_brands").addClass('as-d-none');
            this._quickSearchAttr(brands, "brand-name", value, total_ele);
        } else if(qck_attr.length != 0){
            this.$target.parents().closest(".nav-item").find(".shop_attribs").addClass('as-d-none');
            this._quickSearchAttr(qck_attr, "attrib-name", value, total_ele);
        } else {
            this.$target.parents().closest(".nav-item").find(".shop_tags").addClass('as-d-none');
            this._quickSearchAttr(tags, "tag-name", value, total_ele);
        }
    },
    _asCategChange: function(ev){
        ev.preventDefault();
        var vals = this.$target.find(".as-categ-search").val();
        var total_ele = this.$target.find(".as-categ-search").attr('data-total-ele');
        var cat_list = this.$target.find(".as-categ-search").attr('data-list');
        var categs = this.$target.parents().find(".products_categories").find("input[name='as_category']");
        if (vals == ""){
            this.$target.siblings('form').removeClass('as-d-none');
            this.$target.siblings('.extra-temp').remove();
            $('.no_match_categ').addClass('as-d-none');
        } else {
            var cats = [];
            $.each(categs, function (ind, val) {
                var name = $(val).attr("categ-name");
                name = name.toLowerCase();
                vals = vals.toLowerCase();
                var $main_categ = $(val).parents().closest('li');
                if (name.includes(vals)){
                    cats.push($(val).val());
                }
            });
            var cat_obj = {'category' : cats};
            this._getAlanTemplate("atharva_theme_base","category_search_template",cat_obj).then((res) =>{
                if (this.$target.siblings('.extra-temp')){
                    this.$target.siblings('.extra-temp').remove();
                    this.$target.siblings('form').addClass('as-d-none').after(res['template']);
                } else {
                    this.$target.siblings('form').addClass('as-d-none').after(res['template']);
                }
            });
            if (cats.length){
                $('.no_match_categ').addClass('as-d-none');
            } else {
                $('.no_match_categ').removeClass('as-d-none');
            }
        }
    },
});

publicWidget.registry.asBrandScroll = publicWidget.Widget.extend({
    selector:".as-all-brand-page",
    'events':{
        'click .as-brand-letters > a':'_OnClickBrandItem',
    },
    _OnClickBrandItem : function(ev){
        var brand = this.$target.find(`#${ev.currentTarget.id.charAt(6)}`)[0]
        brand.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
});

});