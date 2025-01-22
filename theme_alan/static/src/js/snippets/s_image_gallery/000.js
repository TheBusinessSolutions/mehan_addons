odoo.define('theme_alan.s_gallery_image',function(require){
'use strict';

var ajax = require('web.ajax');
var publicWidget = require('web.public.widget');
var alanLazy = require("atharva_theme_base.lazy_loader");

publicWidget.registry.AsGalleryImage = alanLazy.extend({
    selector: '.as_image_gallery',
    disabledInEditableMode: false,

    start: function (editable_mode) {
        var cr = this;
        return cr._super.apply(cr, arguments).then(()=>{
            if (cr.editableMode){
                cr.$target.empty().append('<div class="container"><div class="seaction-head"><h3>Image Gallery Snippet</h3></div></div>');
            }
            if (!cr.editableMode) {
                this.getTabData();
            }
        });
    },
    getTabData: function() {
    	var cr = this;
        cr.$target.addClass("as-dynamic-loading");
        ajax.jsonRpc('/get/get_image_tab_content', 'call', {
            'tabData': cr.$target.attr('data-tabData')
        }).then(function(data) {
        	cr.$target.removeClass("as-dynamic-loading").empty().append(data.temp);
            var sliderData = { spaceBetween: 15, slidesPerView: 1,
                breakpoints: {
                    640: {
                      slidesPerView: 1,
                    },
                    768: {
                      slidesPerView: 2,
                    },
                    1024: {
                      slidesPerView: 3,
                    },
                },
                navigation: {
                  nextEl: ".swiper-button-next",
                  prevEl: ".swiper-button-prev",
                },
                scrollbar: {el: ".swiper-scrollbar", hide: false},
            }
            cr.get_tab_data($(cr.$target),sliderData);
        });
    },

    get_tab_data: function(target, data){
        var cr = this;
        $(target).find(".img_tabs").click(function(){
            $(target).find('.img_tabs').removeClass('active');
            $(target).find('.tab-pane').removeClass('active show');
            $(this).addClass('active');
            var $tab = $(target).find('.active');
            var $activeTab = $tab.find('a').attr('href').slice(1);
            var tabContent = $(target).find('div[data-info="'+ $activeTab +'"]');
            tabContent.addClass('active show');
            tabContent.attr("id","cr-swiper1")
            var swiper1 = new Swiper("#cr-swiper1", data);
            tabContent.removeAttr("id");
        });
        if($(target).find(".img_tabs")[0]) {
            $(target).find(".img_tabs")[0].click();
        }
    },
});
});
