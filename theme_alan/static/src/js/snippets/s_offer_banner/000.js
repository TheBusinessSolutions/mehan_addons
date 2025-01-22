odoo.define('theme_alan.s_offer_banner_front',function(require){
'use strict';

var timer;
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");

publicWidget.registry.AsOfferBanner = alanLazy.extend({
    selector: '.as_offer_banner',
    disabledInEditableMode: false,
    start: function (editable_mode) {
        var cr = this;
        if (cr.editableMode){
            clearInterval(timer);
            cr.$target.removeClass("d-none");
            cr.$target.find(".offer_timer_section").empty().append('OFFER TIMER');
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
                this.offerBannerTimer();
            }
        }
    },
    offerBannerTimer: function() {
        var cr = this;
        var offerTime= cr.$target.attr('data-offerTime');
        var date = offerTime
        if(date != 'nan') {
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
                if(distance > 0 && cr.$target.find('.offer_timer_section')) {
                    cr.$target.find('.offer_timer_section').empty();
                    var append_data="<div class='offer_timer_section'><ul contenteditable='false'><li><span>"+ days +"</span><label>Days</label></li><li><span>"+hours+"</span><label>Hours</label></li><li><span>"+minutes+"</span><label>Minutes</label></li><li><span>"+seconds+"</span><label>Seconds</label></li></ul></div>";
                    cr.$target.find('.offer_timer_section').css('display','block');
                    cr.$target.find('.offer_timer_section').append(append_data);
                }
                if(distance < 1000) {
                    cr._clearInter(cr);
                }
            }, 1000);
        }
    },
    _clearInter: function(cr){
        clearInterval(timer);
        cr.$target.addClass("d-none");
    },
});
});