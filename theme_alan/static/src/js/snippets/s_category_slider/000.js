odoo.define('theme_alan.s_cat_slider',function(require){
'use strict';

var ajax = require('web.ajax');
const wSaleUtils = require('website_sale.utils');
const { AjaxAddToCart, alanUpdateCartNavBar }  = require('theme_alan.core_mixins');
const cloneAnimation = wSaleUtils.animateClone;
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");

publicWidget.registry.AsCategorySlider = alanLazy.extend(AjaxAddToCart, {
    selector: '.as_cat_slider, .as_cat_product_slider',
    disabledInEditableMode: false,
    'events':{
        'click a.addToCart':'_prodAddToCart',
    },
    start: function (editable_mode) {
        var cr = this;
        if (cr.editableMode){
            if (cr.$target.hasClass("as_cat_slider")) {
                cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Category Snippet</h3></div></div>');
            } else {
                cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Multi Category Product Snippet</h3></div></div>');
            }
        }
        if (!cr.editableMode) {
            this.getCatData();
        }
    },
    getCatData: function() {
        var cr = this;
        cr.$target.addClass("as-dynamic-loading");
        ajax.jsonRpc('/get/get_cat_brand_slider_content', 'call', {
            'cat_ids': cr.$target.attr('data-cat-ids'),
            'snippet_type': cr.$target.attr('data-snippet-type'),
            'mainUI': cr.$target.attr('data-mainUI'),
            'tabOption': cr.$target.attr('data-tabOption'),
            'styleUI': cr.$target.attr('data-styleUI'),
            'dataCount': cr.$target.attr('data-dataCount'),
            'recordLink': cr.$target.attr('data-recordLink'),
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
            var count = data.dataCount;
            var ui = data.mainUI;
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
                      slidesPerView: data.dataCount,
                    },
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
            if (data.tabOption == 'single' || data.tabOption == undefined) {
                cr.initializeSwiper(sliderData);
            } else {
                cr.get_product_data($(cr.$target), sliderData, ui);
            }
        });
    },
    initializeSwiper: function(data){
        var $slider = this.$target.find(".as-Swiper");
        $slider.attr("id","cr-swiper");
        var swiper = new Swiper("#cr-swiper", data);
        $slider.removeAttr("id");
    },

    get_product_data: function(target, data, ui){
        var cr = this;
        $(target).find(".categ_tabs").click(function(){
            $(target).find('.categ_tabs').removeClass('active');
            $(target).find('.tab-pane').removeClass('active show');
            $(this).addClass('active');
            var $tab = $(target).find('.active');
            var $activeTab = $tab.find('a').attr('href').slice(1);
            var tabContent =  $(target).find('div[data-info="'+ $activeTab +'"]')
            tabContent.addClass('active show');
            if(ui == "slider"){
                tabContent.attr("id","cr-swiper1")
                var swiper1 = new Swiper("#cr-swiper1", data);
                tabContent.removeAttr("id");
            }
        });
        if($(target).find(".categ_tabs")[0]) {
            $(target).find(".categ_tabs")[0].click();
        }
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
