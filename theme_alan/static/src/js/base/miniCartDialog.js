odoo.define('theme_alan.as_mini_cart_base', function (require) {
"use strict";

var Dialog = require('web.Dialog');
const { AjaxAddToCart, alanUpdateCartNavBar }  = require('theme_alan.core_mixins');

var miniCart =  Dialog.extend(AjaxAddToCart, {
    template: 'theme_alan.core_front_dialog',
    xmlDependencies: Dialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_front_dialog.xml', ]),
    events: _.extend({}, Dialog.prototype.events, {
        'click .as_close':'close',
        'click a.js_add_cart_json':'_onUpdateQty',
        'change .js_quantity':'_onChangeQty',
        'click a.js_delete_product':'_onClickRemoveProduct',
        'click .as-cpt-clr-cart':'_asClearCart'
    }),
    willStart:function(){
        return this._super.apply(this, arguments).then(() => {
            this.$modal.addClass("as-mini-cart as-modal").removeClass("o_technical_modal");
        });
    },
    init:function(src, opts){
        let initData = {
            subTemplate: opts.subTemplate || "", renderHeader: 0, renderFooter: 0,
            size:opts.size || 'large' , backdrop: true
        }
        this._super(src, _.extend(initData));
        this.options = opts;
    },
    _onClickRemoveProduct: function (ev) {
        ev.preventDefault();
        $(ev.currentTarget).siblings().find('.js_quantity').val(0).trigger("change");
    },
    _onUpdateQty: function(ev){
        ev.preventDefault();
        var $link = $(ev.currentTarget);
        var $input = $link.closest('.input-group').find('input');
        var min = parseFloat($input.data('min') || 0);
        var max = parseFloat($input.data('max') || Infinity);
        var previousQty = parseFloat($input.val() || 0, 10);
        var quantity = ($link.has('.fa-minus').length ? -1 : 1) + previousQty;
        var newQty = quantity > min ? (quantity < max ? quantity : max) : min;
        if (newQty !== previousQty) {
            $input.val(newQty).trigger('change');
        }
        return false;
    },
    _onChangeQty: function (ev){
        var cr = this;
        const product_id = $(ev.currentTarget).data('productId');
        const line_id = $(ev.currentTarget).data('lineId');
        const setQty = $(ev.currentTarget).val();
        if(setQty == 0){
            $(ev.currentTarget).parents(".as-mc-media").remove();
        }
        cr._alanAddToCart({"product_id": product_id, "set_qty":setQty, "line_id":line_id },).then(data =>{
            if(data.cart_quantity == undefined){
                cr.$el.find("as_close").trigger("click");
                location.reload();
            }
            else{
                alanUpdateCartNavBar(data);
                cr.$el.find(".as-cart-summary").empty().append(data['website_sale.short_cart_summary']);
                cr.$el.find(".as-qty").empty().append(data.cart_quantity);
                if(data.cart_quantity == 1){
                    cr.$el.find(".as-qty-sigl-info").empty().append("item");
                }else{
                    cr.$el.find(".as-qty-sigl-info").empty().append("items");
                }
            }
        })
    },
    _asClearCart:function(){
        this._rpc({route: '/as_clear_cart',params: {}}).then(() => {location.reload()});
    }
});
return miniCart;
});