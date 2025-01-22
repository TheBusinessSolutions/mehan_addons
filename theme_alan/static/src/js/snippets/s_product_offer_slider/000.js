odoo.define('theme_alan.s_product_offer_slider',function(require){
'use strict';

var ajax = require('web.ajax');
var publicWidget = require('web.public.widget');
const wSaleUtils = require('website_sale.utils');
const { AjaxAddToCart, alanUpdateCartNavBar }  = require('theme_alan.core_mixins');
const cloneAnimation = wSaleUtils.animateClone;
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");
var timer = [];
publicWidget.registry.AsProdOfferSliderMulti = alanLazy.extend(AjaxAddToCart, {
    selector: '.as_product_offer_slider',
    disabledInEditableMode: false,
    'events':{
        'click a.addToCart':'_prodAddToCart',
    },
    start: function (editable_mode) {
        var cr = this;
        if (cr.editableMode){
            cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Multi Product Offer Snippet</h3></div></div>');
            cr.$target.removeClass("d-none");
        }
        if (!cr.editableMode) {
            cr.$target.removeClass("d-none");
            this.$target.parents("div#wrap").addClass('js_sale');
            this.getProductOfferData();
        }
    },
    getProductOfferData: function() {
    	var cr = this;
        cr.$target.addClass("as-dynamic-loading");
        ajax.jsonRpc('/get/get_prod_offer_slider_content', 'call', {
            'prod_ids':cr.$target.attr("data-prod-ids"),
            'timerData':cr.$target.attr("data-timerData"),
            'imgPosition':cr.$target.attr("data-imgPosition"),
            'mainUI': cr.$target.attr('data-mainUI'),
            'dataCount': cr.$target.attr('data-dataCount'),
            'cart': cr.$target.attr('data-cart'),
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
        	cr.$target.removeClass("as-dynamic-loading").empty().append(data.template);
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
                    320: {
                      slidesPerView: 1,
                    },
                    768: {
                      slidesPerView: 1,
                    },
                    1024: {
                      slidesPerView: 2,
                    },
                    1200: {
                      slidesPerView: count,
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
                sliderData['autoplay'] = { delay: stimer, disableOnInteraction: false }
            }

            if (data.infinity) {
                sliderData['loop'] = true
            }
            cr.initializeSwiper(sliderData);
            setTimeout(function(){
                cr._loadTimer();
            }, 500);
        });
    },

    initializeSwiper: function(data){
        var $slider = this.$target.find(".as-Swiper");
        $slider.attr("id","cr-swiper");
        var swiper = new Swiper("#cr-swiper", data);
        $slider.removeAttr("id");
    },

    _loadTimer: function(ev){
        var cr = this;
        var timerDiv = $(".timerdiv");
        $.each(timerDiv, function(res){
            var date = $(this).attr('data-timer');
            var prod = $(this).attr('data-prodId');
            if(date != 'nan') {
                var inputDate = new Date(date).getTime();
                var i = "inter";
                eval('var '+ i + prod + '= ' + setInterval(function() {
                    var now = new Date().getTime();
                    var distance = inputDate - now ;
                    if (distance > 0) {
                        cr.$target.parents().find('.offer-product-'+prod).removeClass('d-none');
                        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
                        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
                        var seconds = Math.floor((distance % (1000 * 60)) / 1000);
                        if ((seconds+'').length == 1) {
                            seconds = '0' + seconds;
                        }
                        if ((days+'').length == 1) {
                            days = '0' + days;
                        }
                        if ((hours+'').length == 1) {
                            hours = '0' + hours;
                        }
                        if ((minutes+'').length == 1) {
                            minutes = '0' + minutes;
                        }
                    }
                    if(distance > 0 && cr.$target.find('.timerdiv')) {
                        cr.$target.find('.timer-division-'+prod).empty();
                        var append_data="<div class='timerdiv'><ul contenteditable='false'><li><span>"+ days +"</span><label>Days</label></li><li><span>"+hours+"</span><label>Hours</label></li><li><span>"+minutes+"</span><label>Minutes</label></li><li><span>"+seconds+"</span><label>Seconds</label></li></ul></div>";
                        cr.$target.find('.timer-division-'+prod).css('display','block');
                        cr.$target.find('.timer-division-'+prod).append(append_data);
                    }
                    if(distance < 1000) {
                        timer.push("inter"+prod);
                        cr._clearInter(cr,prod);
                    }
                }, 1000) + ";");
            }
        });
    },

    _clearInter: function(cr,prod){
        var dis = timer.indexOf("inter"+prod);
        clearInterval(timer[dis]);
        cr.$target.parents().find('.offer-product-'+prod).remove();
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
