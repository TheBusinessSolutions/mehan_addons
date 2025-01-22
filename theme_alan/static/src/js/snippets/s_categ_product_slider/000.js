odoo.define('theme_alan.s_cat_prod_slider',function(require){
'use strict';

var ajax = require('web.ajax');
const wSaleUtils = require('website_sale.utils');
const { AjaxAddToCart, alanUpdateCartNavBar }  = require('theme_alan.core_mixins');
const cloneAnimation = wSaleUtils.animateClone;
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");

publicWidget.registry.AsCategProduct = alanLazy.extend(AjaxAddToCart, {
    selector: '.as_categ_slider',
    disabledInEditableMode: false,
    'events':{
        'click a.addToCart':'_prodAddToCart',
    },
    start: function (editable_mode) {
        var cr = this;
        if (cr.editableMode){
            cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Single Category Product Snippet</h3></div></div>');
        }
        if (!cr.editableMode) {
            this.$target.parents("div#wrap").addClass('js_sale');
            this.getCatProdData();
        }
    },
    getCatProdData: function() {
        var cr = this;
        cr.$target.addClass("as-dynamic-loading");
        ajax.jsonRpc('/get/get_cat_prod_slider_content', 'call', {
            'cat_ids': cr.$target.attr('data-cat-ids'),
            'prod_ids': cr.$target.attr('data-prod-ids'),
            'snippet_type': cr.$target.attr('data-snippet-type'),
            'styleUI': cr.$target.attr('data-styleUI'),
            'autoSlider': cr.$target.attr('data-autoSlider'),
            'sTimer': cr.$target.attr('data-sTimer'),
            'cart': cr.$target.attr('data-cart'),
            'quickView': cr.$target.attr('data-quickView'),
            'compare': cr.$target.attr('data-compare'),
            'wishList': cr.$target.attr('data-wishList'),
            'prodLabel': cr.$target.attr('data-prodLabel'),
            'rating': cr.$target.attr('data-rating'),
            'infinity': cr.$target.attr('data-infinity'),
            'sliderType': cr.$target.attr('data-slider'),
        }).then(function(data) {
            cr.$target.removeClass("as-dynamic-loading").empty().append(data.slider);
            var stimer = data.sTimer;
            var sliderData = { spaceBetween: 15, slidesPerView: 1,
                navigation: {
                  nextEl: ".swiper-button-next",
                  prevEl: ".swiper-button-prev",
                },
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
                sliderData.autoplay = {
                  delay: stimer,
                  disableOnInteraction: false,
                }
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
