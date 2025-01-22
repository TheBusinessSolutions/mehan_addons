odoo.define('theme_alan.s_product_banner_slider',function(require){
'use strict';

var ajax = require('web.ajax');
const wSaleUtils = require('website_sale.utils');
const { AjaxAddToCart, alanUpdateCartNavBar }  = require('theme_alan.core_mixins');
const cloneAnimation = wSaleUtils.animateClone;
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");
if($('.oe_website_sale').length === 0){
    $('div#wrap').addClass('oe_website_sale');
}

publicWidget.registry.AsProductBannerSliders = alanLazy.extend(AjaxAddToCart, {
    selector: '.as_product_banner_slider',
    disabledInEditableMode: false,
    'events':{
        'click a.addToCart':'_prodAddToCart',
    },

    start: function (editable_mode) {
        var cr = this;
        return cr._super.apply(cr, arguments).then(()=>{
            if (cr.editableMode){
                cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Product Banner Slider Snippet</h3></div></div>');
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
            'snippet_type': cr.$target.attr('data-snippet-type'),
            'imgPosition': cr.$target.attr('data-imgPosition'),
            'cart': cr.$target.attr('data-cart'),
            'buyNow': cr.$target.attr('data-buyNow'),
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
