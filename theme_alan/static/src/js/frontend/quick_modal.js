odoo.define('theme_alan.quick_modal', function (require) {
'use strict';

var Dialog = require('web.Dialog');

var quick_dialog = Dialog.extend({
	template: 'atharva_theme_base.core_quick_dialog',
	xmlDependencies: Dialog.prototype.xmlDependencies.concat([
        '/atharva_theme_base/static/src/xml/quick_search_modal.xml', ]),
	events: _.extend({}, Dialog.prototype.events, {
        'click .as_close':'close',
        'mouseenter .modal_lst_item': '_enterModalList',
        'mouseleave .modal_lst_item': '_leaveModalList',
        'input .as-datas-search': '_onInputSearch',
        'click .brand_modal_item': '_onClickBrandModalItem',
        'click .as_alpha_find' : '_scrollToBrandCat'
    }),
    willStart:function(){
        return this._super.apply(this, arguments).then(() => {
            this.$modal.addClass("as-cat-quick-search-modal as-modal").removeClass("o_technical_modal");
        });
    },
    init: function (src, opts) {
        this.isWebsite = true;
        let initData = {
                subTemplate: opts.subTemplate || "", renderHeader: 0, renderFooter: 0,
                size:opts.size || 'large', viewType: opts.viewType || false,  backdrop: true
            }
        this._super(src, _.extend(initData));
        this.options = opts;
    },
    _onClickBrandModalItem: function(ev){
        var curr_url = ev.currentTarget.baseURI;
        var item_target = $(ev.currentTarget).children().attr('name');
        var item_id = $(ev.currentTarget).children().attr('id');
        var item_name = $(ev.currentTarget).children().attr('data-name');
        if (item_target == 'category'){
            if (curr_url.includes('/shop/category/')){
                var url_attr = curr_url.split('?')[1];
                var target_url = '/shop/category/'+item_id+'?'+url_attr;
            } else {
                var target_url = '/shop/category/'+item_id;
            }
        } else {
            if (curr_url.includes('?')){
                var target_url = curr_url+'&'+item_target+"="+item_id;
            } else {
                var target_url = curr_url+'?'+item_target+"="+item_id;
            }
        }
        window.location.href = target_url;
    },
    _enterModalList: function(ev){
        var selItem = $(ev.currentTarget).attr("data-item").toLowerCase();
        var selClass = $(ev.currentTarget).attr("data-item").toUpperCase();
        $('.brandHead').addClass('as-quick-filter-blur');
        $.each($('.item_modal'), function(ind, val){
            var item = $(val).attr("data-item").toLowerCase();
            if(selItem == 'hash'){
                $('.hash').removeClass('as-quick-filter-blur');
            } else {
                $('.hash').addClass('as-quick-filter-blur');
            }
            if(item == selItem){
                $('.'+selClass).removeClass('as-quick-filter-blur');
                $(val).parent().addClass('as-quick-filter-highlight');
                $(val).parent().removeClass('as-quick-filter-blur');
            } else {
                $(val).parent().removeClass('as-quick-filter-highlight');
                $(val).parent().addClass('as-quick-filter-blur');
            }
        });
    },
    _leaveModalList: function(ev){
        $('.brandHead').removeClass('as-quick-filter-blur');
        $.each($('.item_modal'), function(ind, val){
            $(val).parent().removeClass('as-quick-filter-highlight');
            $(val).parent().removeClass('as-quick-filter-blur');
        });
    },
    _onInputSearch: function(ev){
        var value = $(ev.currentTarget).val();
        var inputName = "input[name='"+$(ev.currentTarget).attr('data-dataType')+"']";
        var cats = $('.modal_selector').find(inputName);
        $('.as-modal-categ').addClass('as-d-none');
        $('h5').addClass('as-d-none');
        $.each(cats, function(ind, val){
            var name = $(val).attr("data-name");
            name = name.toLowerCase();
            var head = name[0].toUpperCase();
            value = value.toLowerCase();
            if (value == ""){
                $(val).parents('.modal-body').find('h5').removeClass('as-d-none');
                $(val).parents().closest('li').removeClass('as-d-none ct');
            } else {
                if(head != "."){
                    if (name.includes(value)){
                        $('.'+head).removeClass('as-d-none');
                        if (!isNaN(head)) {
                            $('.hash').removeClass('as-d-none');
                        }
                        $(val).parents().closest('li').removeClass('as-d-none ct');
                    } else {
                        $(val).parents().closest('li').addClass('as-d-none ct');
                    }
                }
            }
        });
        var no_cat = $('.ct').length;
        if (no_cat == cats.length){
            $('.no_data').removeClass('as-d-none');
        } else {
            $('.no_data').addClass('as-d-none');
        }
    },
    _scrollToBrandCat:function(ev){
        var alpha_id = "h5#" + $(ev.currentTarget).data("alpha");
        var cur_scl_pos = this.$el.find(".as-quick-search-body").scrollTop();
        var alpha_pos = this.$el.find(alpha_id).position().top
        this.$el.find(".as-quick-search-body").animate({'scrollTop': alpha_pos + cur_scl_pos}, 'slow')
    }
});
return quick_dialog

});