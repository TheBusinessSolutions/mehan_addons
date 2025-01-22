odoo.define('theme_alan.as_quick_product_view', function (require) {
"use strict";

var ajax = require('web.ajax');
var Dialog = require('web.Dialog');
var config = require('web.config');
var VariantMixin = require('website_sale.VariantMixin');
var wSaleUtils = require('website_sale.utils');
const webUtils = require('web.utils');
const cartHandlerMixin = wSaleUtils.cartHandlerMixin;
const { AjaxAddToCart, alanUpdateCartNavBar }  = require('theme_alan.core_mixins');

var addedCart = Dialog.extend({
    template: 'theme_alan.core_front_dialog',
    xmlDependencies: Dialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_front_dialog.xml', ]),
    events: _.extend({}, Dialog.prototype.events, VariantMixin.events, {
        'click .as_close':'close',
    }),
    willStart:function(){
        return this._super.apply(this, arguments).then(() => {
            this.$modal.addClass("as-quick-product-attribute-modal as-modal").removeClass("o_technical_modal");
        });
    },
    init: function (src, opts) {
        this.isWebsite = true;
        let initData = {
                subTemplate: opts.subTemplate || "", renderHeader: 0, renderFooter: 0,
                size:opts.size || 'large', backdrop: true
            }
        this._super(src, _.extend(initData));
        this.options = opts;
    },
})

var quickAddCart =  Dialog.extend(VariantMixin, cartHandlerMixin, AjaxAddToCart,{
    template: 'theme_alan.core_front_dialog',
    xmlDependencies: Dialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_front_dialog.xml', ]),
    events: _.extend({}, Dialog.prototype.events, VariantMixin.events, {
        'click .as_close':'close',
        'click a.js_add_cart_json': 'onClickAddCartJSON',
        'change form .js_product:first input[name="add_qty"]': 'onChangeAddQuantity',
        'click #add_to_cart, .o_we_buy_now': '_onClickAdd',
    }),
    willStart:function(){
        return this._super.apply(this, arguments).then(() => {
            if(this.options.viewType == "quick-add-cart"){
                this.$modal.addClass("as-quick-product-attribute-modal as-modal").removeClass("o_technical_modal");
            }else{
                this.$modal.addClass("as-quick-product-modal fade").removeClass("o_technical_modal");
            }
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
    _toggleDisable: function ($parent, isCombinationPossible) {
        VariantMixin._toggleDisable.apply(this, arguments);
        $parent.find("#add_to_cart").toggleClass('disabled', !isCombinationPossible);
        $parent.find(".o_we_buy_now").toggleClass('disabled', !isCombinationPossible);
    },
    _onChangeCombination: function (ev) {
        VariantMixin._onChangeCombination.apply(this, arguments);
        var combination = arguments[2];
        var free_qty = combination.free_qty;
        if (free_qty < 1 && !combination.allow_out_of_stock_order){
            $('.as-quick-cart').addClass('as-disabled');
            $('.qk_check_product').addClass('as-disabled');
            $('.o_we_buy_now').addClass('as-disabled');
        } else {
            $('.as-quick-cart').removeClass('as-disabled');
            $('.qk_check_product').removeClass('as-disabled');
            $('.o_we_buy_now').removeClass('as-disabled');
        }
    },
    _onClickAdd: function (ev) {
        ev.preventDefault();
        this.asQuickAdd = $(ev.currentTarget).hasClass("as-quick-cart");
        if(this.asQuickAdd == true){
            $(ev.currentTarget).addClass("as-btn-loading")
        }
        this.getCartHandlerOptions(ev);
        return this._handleAdd($(ev.currentTarget).closest('form'));
    },
    _handleAdd: function ($form) {
        var cr = this;
        this.$form = $form;
        var productSelector = [
            'input[type="hidden"][name="product_id"]',
            'input[type="radio"][name="product_id"]:checked'
        ];
        var productReady = this.selectOrCreateProduct(
            $form,
            parseInt($form.find(productSelector.join(', ')).first().val(), 10),
            $form.find('.product_template_id').val(),
            false
        );
        return productReady.then(function (productId) {
            $form.find(productSelector.join(', ')).val(productId);
            cr.rootProduct = {
                product_id: productId,
                quantity: parseFloat($form.find('input[name="add_qty"]').val() || 1),
                product_custom_attribute_values: cr.getCustomVariantValues($form.find('.js_product')),
                variant_values: cr.getSelectedVariantValues($form.find('.js_product')),
                no_variant_attribute_values: cr.getNoVariantAttributeValues($form.find('.js_product'))
            };
            return cr._onPreparedProduct();
        });
    },
    _onPreparedProduct: function () {
        return this._submitQuickModal();
    },
    _submitQuickModal: function () {
        const otps = this.rootProduct;
        const $product = $('#product_detail');
        const productTrackingInfo = $product.data('product-tracking-info');
        if (productTrackingInfo) {
            productTrackingInfo.quantity = otps.quantity;
            $product.trigger('add_to_cart_event', [productTrackingInfo]);
        }
        otps.add_qty = otps.quantity;
        otps.product_custom_attribute_values = JSON.stringify(otps.product_custom_attribute_values);
        otps.no_variant_attribute_values = JSON.stringify(otps.no_variant_attribute_values);
        if(this.asQuickAdd == true){
            otps.force_create = true;
            return this.quickAddCartDialog(otps)
        }else{
            return this.addToCart(otps);
        }
    },
    _updateProductImage: function ($productContainer, displayImage, productId, productTemplateId, newCarousel, isCombinationPossible) {
        var $carousel = $productContainer.find('#o-carousel-product');
        if (window.location.search.indexOf('enable_editor') === -1) {
            var $newCarousel = $(newCarousel);
            $carousel.after($newCarousel);
            $carousel.remove();
            $carousel = $newCarousel;
            $carousel.carousel(0);
            this._startZoom();
            this.trigger_up('widgets_start_request', {$target: $carousel});
        }
        $carousel.toggleClass('css_not_available', !isCombinationPossible);
    },
    _startZoom: function () {
        if (!config.device.isMobile) {
            var autoZoom = $('.ecom-zoomable').data('ecom-zoom-auto') || false,
            attach = '#o-carousel-product';
            _.each($('.ecom-zoomable img[data-zoom]'), function (el) {
                onImageLoaded(el, function () {
                    var $img = $(el);
                    $img.zoomOdoo({event: autoZoom ? 'mouseenter' : 'click', attach: attach});
                    $img.attr('data-zoom', 1);
                });
            });
        }
        function onImageLoaded(img, callback) {
            $(img).on('load', function () {
                callback();
            });
            if (img.complete) {
                callback();
            }
        }
    },
    quickAddCartDialog:function(params){
        var cr = this;
        params.add_qty = params.quantity || 1;
        cr._alanAddToCart(params).then(data =>{
            alanUpdateCartNavBar(data);
            var cartQuant = data.cart_quantity;
            var totalAmount = webUtils.Markup($(data["website_sale.short_cart_summary"]).find("#order_total").find(".monetary_field").html());
            ajax.jsonRpc('get/quick_product_view', 'call',{
                'hasVariant':false,
                'productId':params.product_id,
                'viewType':'as-quick-add-to-cart',
                'cartQuant':cartQuant,
                'totalAmount':totalAmount,
            }).then(function(res){
                if(params.show_direct == true){
                    cr.close()
                    var showAddCart = new addedCart(cr,{
                        subTemplate:webUtils.Markup(res['template']),
                        size:'small',
                    })
                    showAddCart.open();
                    $(params.currentTarget).removeClass("as-btn-loading")
                }else{
                    cr.$el.empty().append(res['template']);
                }
            })
        })
    }
});
return quickAddCart
});