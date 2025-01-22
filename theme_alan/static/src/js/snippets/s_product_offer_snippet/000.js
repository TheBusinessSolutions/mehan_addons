odoo.define('theme_alan.s_product_offer',function(require){
'use strict';

var ajax = require('web.ajax');
var timer;
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");

publicWidget.registry.AsProductOffer = alanLazy.extend({
    selector: '.as_product_offer',
    disabledInEditableMode: false,
    start: function (editable_mode) {
        var cr = this;
        if (cr.editableMode){
            cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Single Product Offer Snippet</h3></div></div>');
            cr.$target.removeClass("d-none");
        }
        if (!cr.editableMode) {
            var now = new Date().getTime();
            var offer_date = cr.$target.attr('data-offertime');
            var offer_time = new Date(offer_date).getTime();
            if (now > offer_time) {
                cr.$target.addClass("d-none");
            }
            else{
                cr.$target.removeClass("d-none");
                this.getProductOfferData();
            }
        }
    },
    getProductOfferData: function() {
    	var cr = this;
        cr.$target.addClass("as-dynamic-loading");
        ajax.jsonRpc('/get/get_product_offer_content', 'call', {
            'prod_ids': cr.$target.attr('data-prod-ids'),
            'imgPosition': cr.$target.attr('data-imgPosition'),
            'offerTime': cr.$target.attr('data-offerTime'),
            'cart': cr.$target.attr('data-cart'),
            'buyNow': cr.$target.attr('data-buyNow'),
            'prodLabel': cr.$target.attr('data-prodLabel'),
            'rating': cr.$target.attr('data-rating'),
        }).then(function(data) {
        	cr.$target.removeClass("as-dynamic-loading").empty().append(data.template);
            var date = data.offerTime;
            if(date != 'nan') {
                var breaker = 0;
                var inputDate = new Date(date).getTime();
                timer = setInterval(function() {
                    var now = new Date().getTime();
                    var distance = inputDate - now ;
                    if (distance > 0) {
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
                    if(distance > 0 && cr.$target.find('.timerDiv')) {
                        cr.$target.find('.timerDiv').empty();
                        var append_data="<div class='timerDiv'><ul contenteditable='false'><li><span>"+ days +"</span><label>Days</label></li><li><span>"+hours+"</span><label>Hours</label></li><li><span>"+minutes+"</span><label>Minutes</label></li><li><span>"+seconds+"</span><label>Seconds</label></li></ul></div>";
                        cr.$target.find('.timerDiv').css('display','block');
                        cr.$target.find('.timerDiv').append(append_data);
                    }
                    if(distance < 1000) {
                        cr._clearInter(cr);
                    }
                }, 1000);
            }
        });
    },
    _clearInter: function(cr){
        clearInterval(timer);
        cr.$target.parents().find('.as-product-offer-snippet').remove();
    },
});
});
