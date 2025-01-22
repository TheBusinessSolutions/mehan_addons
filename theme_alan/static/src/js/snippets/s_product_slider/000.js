odoo.define('theme_alan.s_product_slider',function(require){
'use strict';

var ajax = require('web.ajax');
const wSaleUtils = require('website_sale.utils');
const { AjaxAddToCart, alanUpdateCartNavBar }  = require('theme_alan.core_mixins');
const cloneAnimation = wSaleUtils.animateClone;
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");

publicWidget.registry.AsProductSlider = alanLazy.extend(AjaxAddToCart, {
    selector: '.as_product_slider, .as_product_variant_slider, .as_best_seller_product, .as_latest_product',
    disabledInEditableMode: false,
    'events':{
        'click a.addToCart':'_prodAddToCart',
    },
    start: function (editable_mode) {
        var cr = this;
        return cr._super.apply(cr, arguments).then(()=>{
            if (cr.editableMode){
                if (cr.$target.hasClass("as_product_slider")){
                    cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Product Snippet</h3></div></div>');
                } else if (cr.$target.hasClass("as_product_variant_slider")){
                    cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Product Variant Snippet</h3></div></div>');
                } else if (cr.$target.hasClass("as_best_seller_product")){
                    cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Best Seller Product Snippet</h3></div></div>');
                } else if (cr.$target.hasClass("as_latest_product")){
                    cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Latest Product Snippet</h3></div></div>');
                }
            }
            if (!cr.editableMode) {
                this.getProductData();
                this.$target.parents("div#wrap").addClass('js_sale');
            }
        });
    },
    getProductData: function() {
    	var cr = this;
        cr.$target.addClass("as-dynamic-loading");
        ajax.jsonRpc('/get/get_product_slider_content', 'call', {
            'prod_ids': cr.$target.attr('data-prod-ids'),
            'totalCount': cr.$target.attr('data-totalCount'),
            'snippet_type': cr.$target.attr('data-snippet-type'),
            'mainUI': cr.$target.attr('data-mainUI'),
            'styleUI': cr.$target.attr('data-styleUI'),
            'imgPosition': cr.$target.attr('data-imgPosition'),
            'dataCount': cr.$target.attr('data-dataCount'),
            'cart': cr.$target.attr('data-cart'),
            'buyNow': cr.$target.attr('data-buyNow'),
            'quickView': cr.$target.attr('data-quickView'),
            'compare': cr.$target.attr('data-compare'),
            'wishList': cr.$target.attr('data-wishList'),
            'prodLabel': cr.$target.attr('data-prodLabel'),
            'rating': cr.$target.attr('data-rating'),
            'infinity': cr.$target.attr('data-infinity'),
            'autoSlider': cr.$target.attr('data-autoSlider'),
            'sTimer': cr.$target.attr('data-sTimer'),
            'sliderType': cr.$target.attr('data-slider'),
        }).then(function(data) {
        	cr.$target.removeClass("as-dynamic-loading").empty().append(data.slider);
            var count = data.dataCount;
            if(count == undefined) {
                count = 1;
            }
            var stimer = data.sTimer;
            var sliderData = { spaceBetween: 15, slidesPerView: 2,
                navigation: {
                  nextEl: ".swiper-button-next",
                  prevEl: ".swiper-button-prev",
                },
                breakpoints: {
                    640: {
                      slidesPerView: 2,
                    },
                    768: {
                      slidesPerView: 3,
                    },
                    1024: {
                      slidesPerView: 4,
                    },
                    1200: {
                      slidesPerView: count,
                    },
                },
                observer: true,
                observeSlideChildren: true,
                observeParents: true,
            }
            switch (data.sliderType) {
                case 1:
                    sliderData['pagination'] = {}
                    break;
                case 2:
                    sliderData['pagination'] = {el: ".swiper-pagination", clickable: true}
                    break;
                case 3:
                    sliderData['pagination'] = {el: ".swiper-pagination", dynamicBullets: true}
                    break;
                case 4:
                    sliderData['pagination'] = {el: ".swiper-pagination", type: "progressbar"}
                    break;
                case 5:
                    sliderData['pagination'] = {el: ".swiper-pagination", type: "fraction"}
                    break;
                case 6:
                    sliderData['pagination'] = {el: ".swiper-pagination", clickable: true,
                                                renderBullet: function (index, className) {
                                                    return '<span class="' + className + '">' + (index + 1) + "</span>";
                                                }}
                    break;
                case 7:
                    sliderData['scrollbar'] = {el: ".swiper-scrollbar", hide: true}
                    break;
            }
            if (data.autoSlider) {
                sliderData['autoplay'] = { delay: stimer, disableOnInteraction: false }
            }

            if (data.infinity) {
                sliderData['loop'] = true
            }
            cr.initializeSwiper(sliderData);
        });
    },

    initializeSwiper: function(data){
        var $slider = this.$target.find(".as-Swiper");
        $slider.attr("id","cr-swiper");
        var swiper = new Swiper("#cr-swiper", data);
        $slider.removeAttr("id");
    },

    _prodAddToCart: function(ev){
        var product_id = parseInt($(ev.currentTarget).attr('data-product-product-id'));
        this._alanAddToCart({"product_id" : product_id, "add_qty":1}).then(data =>{
            cloneAnimation($('header .o_wsale_my_cart').first(), this.$(ev.currentTarget).closest('form').find('.as-product-img'), 25, 40);
            alanUpdateCartNavBar(data);
        })
    },
});
});
