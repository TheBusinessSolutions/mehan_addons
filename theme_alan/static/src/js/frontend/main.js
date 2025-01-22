odoo.define('theme_alan.frontend_js', function (require) {
"use strict";

var publicWidget = require('web.public.widget')
var Dialog = require('web.Dialog');
var wSaleUtils = require('website_sale.utils');
var webUtils = require('web.utils');
var ajax = require('web.ajax');
require("website_sale_wishlist.wishlist");
var VariantMixin = require('website_sale.VariantMixin');
var quickProdView = require('theme_alan.as_quick_product_view');
var alanMiniCart  = require('theme_alan.as_mini_cart_base');
var alanLazy = require("atharva_theme_base.lazy_loader");
var { AlanTemplateGetter, FetchProductsData, FetchCategoryData,BaseAlanQweb,
    AjaxAddToCart, alanUpdateCartNavBar } = require("theme_alan.core_mixins");

const webTime = require('web.time');
const { _t, qweb } = require('web.core');
const combinationVariant = VariantMixin._onChangeCombination;

var AsOfferCounter = setInterval(function () { }, 1);
var url = window.location.href;
var call = false;

var AlanLogin =  Dialog.extend({
    template: 'theme_alan.core_front_dialog',
    xmlDependencies: Dialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_front_dialog.xml', ]),
    events: _.extend({}, Dialog.prototype.events, {
        'click .as_close':'close',
        'click .loginbtn':'_checkAuthentication',
        'click .haveAccount':'_backToLogin',
        'click .signupbtn':'_userSignup',
    }),
    willStart:function(){
        return this._super.apply(this, arguments).then(() => {
            this.$modal.addClass("as-login-modal as-side-modal as-modal").removeClass("o_technical_modal");
        })
    },
    init: function (src, opts) {
        let initData = { subTemplate: opts.subTemplate || "", renderHeader: 0, renderFooter: 0, backdrop: true }
        this._super(src, _.extend(initData));
        this.options = opts;
    },
    _checkAuthentication:function(ev){
        var cr = this;
        const login = cr.$el.find("#login").val();
        const password = cr.$el.find("#password").val();

        if(login.trim() != "" && password.trim() != ""){
            ev.preventDefault();
            return cr._rpc({
                route: "/alan/login/authenticate",
                params: { "login":login, "password":password }
            }).then(function (result) {
                if(result["login_success"] == true){
                    window.location.reload();
                }
                else if("error" in result){
                    cr.$el.find("#errormsg").css("display","block").empty().append(result["error"]);
                }
            });
        }
    },
    _userSignup:function(ev){
        var cr = this;
        const logins = cr.$el.find("#logins").val();
        const passwords = cr.$el.find("#passwords").val();
        const names = cr.$el.find("#names").val();
        const confirm_passwords = cr.$el.find("#confirm_passwords").val();
        const token = cr.$el.find("#token").val()
        if(logins.trim() != "" && passwords.trim() != ""
            && confirm_passwords.trim() != "" && names.trim() != ""){
            ev.preventDefault();
            return cr._rpc({
                route: "/alan/signup/authenticate",
                params: {
                        "login":logins,
                        "name":names,
                        "password":passwords,
                        "confirm_password":confirm_passwords,
                        "token":token
                    }
            }).then(function (result) {
                if("error" in result){
                    cr.$el.find("#errors").css("display","block").empty().append(result["error"])
                }
                else if(result["signup_success"] == true){
                    window.location.reload();
                }
            });
        }
    },
    _backToLogin:function(){
        this.$el.find("#as-login").click();
    },
});

var similarProduct =  Dialog.extend(VariantMixin, {
    template: 'theme_alan.core_front_dialog',
    xmlDependencies: Dialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_front_dialog.xml', ]),
    events: _.extend({}, Dialog.prototype.events, { 'click .as_close':'close' }),
    willStart:function(){
        return this._super.apply(this, arguments).then(() => {
            this.$modal.addClass("as-similar-product-modal as-side-modal as-modal").removeClass("o_technical_modal");
        })
    },
    init: function (src, opts) {
        let initData = { subTemplate: opts.subTemplate || "", renderHeader: 0, renderFooter: 0, backdrop: true }
        this._super(src, _.extend(initData));
        this.options = opts;
    },
});

publicWidget.registry.as_core = publicWidget.Widget.extend(AlanTemplateGetter,
    FetchProductsData, FetchCategoryData, BaseAlanQweb, AjaxAddToCart, {
    selector:'#wrapwrap',
    events:{
        'click .as-login':'_loginPopup',
        'click a.as-quick-submit': '_quickAddToCart',
        'mouseenter .nav-item':'_check_megamenu',
        'click .as-mini-cart':'_openMiniCart',
        "click a.as-quick-view": "_quickView",
        'submit .as_attributes':'_ajax_attrib_filter',
        'click a.img-gallery-tag':'_productImageClick',
        'click a.video-gallery-tag':'_productVideoClick',
    },
    start:function(){
        this.call_meg = 0;
        this._super.apply(this, arguments);
    },
    _productVideoClick:function(e){
        e.preventDefault();
        $(e.currentTarget).parent().magnificPopup({
            delegate: 'a',
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });
    },
    _productImageClick:function(e){
        e.preventDefault();
        $(e.currentTarget).parent().parent().magnificPopup({
            delegate: 'a',
            type: 'image',
            gallery: {
                enabled: true,
            }
        })
    },
    _ajax_attrib_filter:function(ev){
        ev.preventDefault();
        var cr = this;
        var actionUrl =  location.origin + location.pathname + "?" + $(ev.currentTarget).serialize();
        window.history.pushState("data","Title", actionUrl);
        var cr_shop_state = cr.$target.find("#wrap");
        $("#wrap").before("<div id='as-loader'> <i class='fa fa-circle-o-notch fa-spin fa-3x fa-fw margin-bottom'></i></div>");

        $.ajax({
            url: actionUrl,
            type: 'GET',
            success: function (response) {
                cr_shop_state.empty().replaceWith($(response).find("main").html());
                cr.trigger_up('widgets_start_request', {
                    $target: $('#wrapwrap'),
                });
                $("#as-loader").remove();
                $("html, body").animate({ scrollTop: 0 }, "slow");
            }
        });
    },
    _loginPopup:function(ev){
        var cr = this;
        var cur_ev = ev.currentTarget;
        $(cur_ev).addClass("as-btn-loading");
        cr._rpc({
            route: '/alan/login/',
            params: { }
        }).then(function (response) {
            $(cur_ev).removeClass("as-btn-loading");
            var alanLogin = new AlanLogin(cr,{subTemplate:webUtils.Markup(response['template'])});
            alanLogin.open();
        });
    },
    _quickView:function(ev){
        var productId = $(ev.currentTarget).attr('data-product-id');
        $(ev.currentTarget).addClass("as-btn-loading");
        var self = this;
        return this._rpc({
            route: '/get/quick_product_view',
            params: {'productId':productId ,'viewType':'as-quick-view'}
        }).then(function (response) {
            var quickView = new quickProdView(this,{
                    subTemplate:webUtils.Markup(response['template']),
                    size:'extra-large',
                    viewType:'quick-view'
                });
            quickView.open();
            $(ev.currentTarget).removeClass("as-btn-loading");
            quickView.opened().then(() => {
                self.trigger_up('widgets_start_request', {
                    $target: $("#product_detail"),
                });
            });
        });
    },
    _quickAddToCart:function(ev){
        $(ev.currentTarget).addClass("as-btn-loading");
        var hasVariant = $(ev.currentTarget).attr('data-has-variant');
        var productId = $(ev.currentTarget).attr('data-product-id');
        if(hasVariant != "False"){
            this._quickVariantView(ev, hasVariant, productId);
        }else{
            var qac = new quickProdView(this,{});
            qac.quickAddCartDialog({'product_id':productId, 'show_direct':true,"currentTarget": ev.currentTarget});
        }
    },
    _quickVariantView:function(ev, hasVariant, productId){
        var self = this;
        return this._rpc({
            route: '/get/quick_product_view',
            params: { 'hasVariant':hasVariant, 'productId':productId ,'viewType':'as-quick-add-to-cart'}
        }).then(function (response) {
            var qac = new quickProdView(this,{
                    subTemplate: webUtils.Markup(response['template']),
                    size:'large',
                    viewType:'quick-add-cart'
                });
            qac.open();
            qac.opened(() =>{
                self.trigger_up('widgets_start_request', {
                    $target: qac.$modal.find(".show-extra-prod-info"),
                });
            })
            $(ev.currentTarget).removeClass("as-btn-loading");
        });
    },
    _check_megamenu:function(ev){
        if(this.call_meg == 0){
            if($(ev.currentTarget).hasClass("dropdown")){
                this.getMegaContent(ev);
                this.call_meg = 1;
            }
        }
    },
    getMegaContent: function(ev) {
        var cr = this;
        var $cr = $(ev.currentTarget).find(".as-dynamic-megamenu");
        var contentType = $cr.attr("data-mega-popup");
        var mega_ui = $cr.attr("data-mega-ui");
        var col_ui = $cr.attr("data-col-ui");
        if (contentType == "product_mega_modal" || contentType == "theme_alan.product_mega_modal") {
            var prod_ids = $cr.attr("data-record-ids");
            var mega_view = $cr.attr("data-prod-mega-view");
            cr._fetchProductRawData(prod_ids,"product.template").then((rec) =>{
                if(rec != undefined){
                    let clean_res = []
                    rec.forEach(ele => {
                        ele['price'] = webUtils.Markup(ele['price'])
                        clean_res.push(ele);
                    })
                    let data = { "mega_ui":mega_ui, "prod_ids":prod_ids, "col_ui":col_ui,
                        "mega_data":clean_res, 'is_dynamic':true }
                    if(mega_view == "list"){
                        cr._getAlanTemplate("atharva_theme_base","as_mm_product_list",data).then((res) =>{
                            $cr.empty().append(res['template']);
                        });
                    }else if(mega_view == "grid"){
                        cr._getAlanTemplate("atharva_theme_base","as_mm_product_grid",data).then((res) =>{
                            $cr.empty().append(res['template']);
                        });
                    }else{
                        alert("Something went wrong!")
                    }
                }
            });
        }
        else if(contentType == "category_mega_modal" || contentType == "theme_alan.category_mega_modal"){
            var view = $cr.attr("data-cat-mega-view");
            var cat_data = $cr.attr("data-record-ids");
            var cat_ids = $cr.attr("data-cat-seq");
            if (cat_data != undefined){
                var catData = cat_data.replace(/'/g, '"');
                cr._fetchMegaCategoryTemplate(view,catData,mega_ui,col_ui,cat_ids).then((rec) => {
                    $cr.empty().append(rec['template']);
                });
            }
        }
    },
    _openMiniCart:function(ev){
        $(ev.currentTarget).addClass("as-btn-loading")
        this._alanMiniCart().then((response) => {
            var miniCart = new alanMiniCart(this,{
                subTemplate:webUtils.Markup(response['template']),
                size:'large',
            });
            miniCart.open();
            $(ev.currentTarget).removeClass("as-btn-loading")
        })
    }
});


publicWidget.registry.as_product_details = publicWidget.Widget.extend(AjaxAddToCart, {
    selector:".as-product-detail",
    'events':{
        'click a#add_to_cart_cp_btn':'_stickyAddToCart',
        'click .as-scroll-top':'_asScrollTop',
        'click a#buy_now_cp_btn':'_stickyBuyNow',
        'click .o_website_rating_static':'_productRating',
        'scroll':'_stickyCart'
    },
    start: function () {
        return this._super.apply(this, arguments).then(() => {
            var alterna_and_access = new Swiper(".as-al-ass-swiper", {
                slidesPerView: 2,
                spaceBetween: 10,
                navigation: {
                  nextEl: ".swiper-button-next",
                  prevEl: ".swiper-button-prev",
                },
                breakpoints: {
                  640: {
                    slidesPerView: 2,
                  },
                  768: {
                    slidesPerView: 4,
                  },
                  1024: {
                    slidesPerView: 3,
                  },
                },
            });
        });
    },


    _stickyAddToCart:function(ev){
        const product_id = $(ev.currentTarget).closest("form").find("input[name='product_id']").val();
        this._alanAddToCart({"product_id" : product_id,"add_qty":1}).then(data =>{
            alanUpdateCartNavBar(data);
            location.href = "/shop/cart";
        })
    },
    _stickyBuyNow:function(){
        this.$target.find(".o_we_buy_now").trigger("click");
    },
    _asScrollTop:function (ev) {
        $("html, body").animate({ scrollTop: 0 }, "slow");
    },
    _productRating:function(ev){
        this.$target.find("#nav_tabs_link_3").trigger("click");
    },
    _stickyCart:function(ev){
        var cr = this;
        var addToCartBtns = cr.$target.find('#add_to_cart');
        if(cr.$target.find('.as-sticky-cart-active').length != 0 && addToCartBtns.length != 0){
            const top = cr.$target.find('#add_to_cart').offset().top;
            const bottom = cr.$target.find('#add_to_cart').offset().top + cr.$target.find('#add_to_cart').outerHeight();
            const bottom_screen = $(window).scrollTop() + $(window).innerHeight();
            const top_screen = $(window).scrollTop();
            if ((bottom_screen > top) && (top_screen < bottom)){
                if(cr.$target.find('.as-product-sticky-cart').hasClass("as-stikcy-show")){
                    cr.$target.find('.as-product-sticky-cart').removeClass("as-stikcy-show");
                }
            } else {
                if(top < 0){
                    if(!cr.$target.find('.as-product-sticky-cart').hasClass("as-stikcy-show")){
                        cr.$target.find('.as-product-sticky-cart').addClass("as-stikcy-show");
                    }
                }
            }
        }
        var offset = 450;
        var $back_to_top = $('.as-scroll-to-top');
        ($('#wrapwrap').scrollTop() > offset) ? $back_to_top.addClass('as-bt-visible'): $back_to_top.removeClass('as-bt-visible');
    },
});

publicWidget.registry.ajaxProductLoadAuto = publicWidget.Widget.extend({
    selector:'.as-shop',
    events:{
        'click a.o_alter_view':'_getAlternativeProduct',
        'click .as-clear-filter':'_clearFilter',
        'mouseenter .css_attribute_color_tag': '_onMouseEnterColorAttribute',
        'mouseleave .css_attribute_color_tag': '_onMouseOutColorAttribute',
    },
    start:function(){
        $('.as-shop-tags').tooltip({
            template: '<div class="tooltip as-tooltip-white"><div class="arrow"></div><div class="tooltip-inner"></div></div>'
          })

        this.$target.on('scroll', _.throttle(function (ev) {
            if($('.as_load_product').offset() != undefined){
                var gettop = $('.as_load_product').offset().top;
                var getheight = $('.as_load_product').outerHeight();
                var getwindowheight = $(window).height();
                var nxtbtnpos = gettop+getheight-getwindowheight;
                if (nxtbtnpos < 30){
                    if(call != true){
                        $('.as_load_product').click();
                        call = true;
                    }
                }else{
                    call = false;
                }
            }
        }, 15));
        return this._super.apply(this, arguments).then(() => {
            var catgeory_tag  = new Swiper('.as-shop-top-cat-slider',{
                navigation: {
                    nextEl: ".swiper-button-next",
                    prevEl: ".swiper-button-prev",
                },
                slidesPerView: "auto",
                spaceBetween: 10,
          })
        })
    },
    _clearFilter:function(ev){
        const fieldName = $(ev.currentTarget).data("name");
        const fieldValue = $(ev.currentTarget).data("value");
        const $filterForm = this.$target.find("form.js_attributes");
        const $input = $filterForm.find('input[name="'+fieldName+'"][value="' + fieldValue + '"]');
        if($input.length == 0){
            const $option = $filterForm.find('option[value=' + fieldValue + ']');
            $option.closest('select').val('');
        }
        $input.prop('checked', false);
        $filterForm.submit();
    },
    _onMouseEnterColorAttribute :function (ev) {
        this.$target.find('.css_attribute_color')
            .removeClass("active")
        this.$target.find('.js_variant_change').attr('checked', false);
        $(ev.currentTarget).find('span').attr('checked', true);
        $(ev.currentTarget).addClass("active");

        var VariantImgUrl = $(ev.currentTarget).find('span').attr('data-src');
        var $Image = $(ev.relatedTarget).parents('.o_wsale_product_grid_wrapper').find('div.oe_product_image').find('img').eq(0);
        $Image.attr('src',VariantImgUrl);
    },
    _onMouseOutColorAttribute :function (ev) {
        var ProductImgUrl = $(ev.currentTarget).find('span').attr('product_image');
        var $Image = $(ev.relatedTarget).parents('.o_wsale_product_grid_wrapper').find('div.oe_product_image').find('img').eq(0);
        this.$target.find('.css_attribute_color_tag')
            .removeClass("active")
        $Image.attr('src',ProductImgUrl);
    },
    _getAlternativeProduct:function(ev){
        var cr = this;
        var prod_temp_id = $(ev.currentTarget).attr('data-product_template_id');
        $(ev.currentTarget).addClass("as-btn-loading");
        cr._rpc({
            route: '/json/alternative_product/',
            params: { 'prod_tmp_id':prod_temp_id }
        }).then(function (response) {
            var similarDialog = new similarProduct(cr,{
                subTemplate:webUtils.Markup(response['quickAlterTemp'])});
                similarDialog.open();
                $(ev.currentTarget).removeClass("as-btn-loading");
        });
    }
});

publicWidget.registry.alan_quick_product_load = alanLazy.extend({
    "selector": ".as_load_product",
    events : {
        "click": "_loadProduct"
    },
    _loadProduct:function(ev){
        var cr = this;
        var page = 1 +  parseInt(this.$el.attr("page"));
        var path = $($(".products_pager").find("li")[page]).find("a").attr("href");
        var actionUrl = window.location.origin + path;
        var $product_tbody = $(".o_wsale_products_grid_table_wrapper").find("tbody");
        $(".o_wsale_products_grid_table_wrapper").find(".load_next_product").remove();;
        var $product_pager = $(".products_pager");
        $.ajax({
            url: actionUrl,
            type: 'GET',
            success: function (response) {
                var products = $(response).find(".o_wsale_products_grid_table_wrapper").find("tbody").html();
                var pager = $(response).find(".products_pager").html();
                $product_tbody.append(products)
                $($product_pager).empty().append(pager);
                cr.trigger_up('widgets_start_request', {
                    $target: $('.as-shop'),
                });
                cr.trigger_up('widgets_start_request', {
                    $target: $('.as_load_product'),
                });
            }
        });
        var maxpage = cr.$el.attr("max_page");
        cr.$el.attr("page",page);
        if(page == maxpage){cr.$el.remove();}
        var checkurl = url.split("/");
        var checkattrurl = url.split("=");
        var url_have_page = false;
        if(checkattrurl.length > 1){
            var spliturl = url.split("?");
            var checksuburl = spliturl[0].split("/");
            for (let index = 0; index < checksuburl.length; index++){
                if(checksuburl[index] == "page"){
                    url_have_page = true;
                }
            }
            if(url_have_page != true){
                var new_url =  checksuburl.join("/") + "/page/" + page + "?" +spliturl[1];
            }else{
                checksuburl.pop();
                checksuburl.push(page);
                var new_url = checksuburl.join("/") + "?" +spliturl[1];
            }
        }else{
            for (let index = 0; index < checkurl.length; index++) {
                if(checkurl[index] == "page"){
                    url_have_page = true;
                }
            }
            if(url_have_page != true){
                var new_url = url + "/page/" + page;
            }else{
                checkurl.pop();
                checkurl.push(page);
                var new_url = checkurl.join("/");
                }
            }
        window.history.pushState("data","Title",new_url);
    },
});


publicWidget.registry.alan_product_offers = alanLazy.extend({
    "selector": ".show-extra-prod-info",
    events : {
        "click": "_showOffers"
    },
    _showOffers: function(){
        var self = this;
        this._rpc({
            route: '/product/offer',
            params: {'offer_id': this.$target.attr("data-info_id")},
        }).then((res) =>{
            this.offer_dialog = new Dialog(self, {
                technical: false,
                $content: $('<div/>').html(res['data']),
                renderFooter: false,
                renderHeader: false,
                backdrop: true
            }).open();
            this.offer_dialog.opened().then(() => {
                this.trigger_up('widgets_start_request', {
                    $target: this.offer_dialog.$modal,
                });
            });

        })
    }
});

publicWidget.registry.ProductWishlist.include({
    events: _.extend({
        'click .wishlist-section .as-wishlst-rm': '_removeWishlistItem',
        'click .wishlist-section .as-wishlst-add': '_addWishlistItem',
    }, publicWidget.registry.ProductWishlist.prototype.events),
    _removeWishlistItem:function (e, deferred_redirect) {
        var $div = $(e.currentTarget).parent().parent().parent();
        var wish = $div.data('wish-id');
        var product = $div.data('product-id');
        var self = this;
        this._rpc({
            route: '/shop/wishlist/remove/' + wish,
        }).then(function () {
            $div.remove();
        });
        this.wishlistProductIDs = _.without(this.wishlistProductIDs, product);
        if (this.wishlistProductIDs.length === 0) {
            if (deferred_redirect) {
                deferred_redirect.then(function () {
                    self._redirectNoWish();
                });
            }
        }
        this._updateWishlistView();
    },
    _asAddOrMoveWish:function(e){
        var $navButton = $('header .o_wsale_my_cart').first();
        var div = $(e.currentTarget).parent().parent().parent().parent();
        var product = div.data('product-id');
        var wish = div.data('wish-id');
        $('.o_wsale_my_cart').removeClass('d-none');
        wSaleUtils.animateClone($navButton, div, 25, 40);
        if ($('#b2b_wish').is(':checked')) {
            return this._addToCart(product, div.find('add_qty').val() || 1);
        } else {
            var adding_deffered = this._addToCart(product, div.find('add_qty').val() || 1);
            this._rpc({
                route: '/shop/wishlist/remove/' + wish,
            }).then(function () {
                div.remove();
            });
            return adding_deffered;
        }
    },
    _addWishlistItem:function(ev){
        var self = this;
        this.$('.wishlist-section .as-wishlst-add').addClass('disabled');
        this._asAddOrMoveWish(ev).then(function () {
            self.$('.wishlist-section .as-wishlst-add').removeClass('disabled');
            $(ev.currentTarget).parent().parent().find(".as-wishlst-rm").trigger('click')
        });
    }
})

ajax.loadXML('/theme_alan/static/src/xml/counters.xml', qweb)
VariantMixin._onChangeCombination = function (ev, $parent, combination) {
    var self = this;
    if (combination['is_combination_possible'] === true) {
        try {
            this._rpc({
                route: '/get_offer_ids',
                params: {
                    'product_id': combination['product_id'],
                    'product_template_id': combination['product_template_id']
                },
            }).then((data) => {
                if(data){
                    if ((combination['has_discounted_price'] === true || data['offer'].has_future_offer === true || data['offer'].discount_include == 'with_discount') && data !== false && combination['is_combination_possible'] === true) {
                        self.$target.find('#as_product_offer').empty().html(qweb.render('theme_alan.as_countdown_template', { data: data, combination: combination }));
                        clearInterval(AsOfferCounter);
                        var offerTimer = function(){
                            var offerTime = moment(webTime.str_to_datetime(data['offer'].date_end));
                            var currTime = moment();
                            var asTime = moment.duration(offerTime - currTime);
                            asTime = moment.duration(asTime.asMilliseconds() - 1000, 'milliseconds');
                            if (asTime.asMilliseconds() < 0) {
                                clearInterval(AsOfferCounter);
                                self.$target.find('#as_product_offer').empty();
                            }else{
                                var days = parseInt(moment.duration(asTime).asDays());
                                var hours = moment.duration(asTime).hours();
                                var minutes = moment.duration(asTime).minutes();
                                var seconds = moment.duration(asTime).seconds();
                                days = days < 10 ? "0" + days : days;
                                hours = hours < 10 ? "0" + hours : hours;
                                minutes = minutes < 10 ? "0" + minutes : minutes;
                                seconds = seconds < 10 ? "0" + seconds : seconds;
                                self.$target.find('#as_countdown_div').empty().html("<ul>\
                                    <li>\
                                        <label>"+ days +"</label>\
                                        <span>Days</span>\
                                    </li>\
                                    <li>\
                                        <label>"+ hours +"</label>\
                                        <span>Hours</span>\
                                    </li>\
                                    <li>\
                                        <label>"+ minutes +"</label>\
                                        <span>Minutes</span>\
                                    </li>\
                                    <li>\
                                        <label>"+ seconds +"</label>\
                                        <span>Seconds</span>\
                                    </li>\
                                </ul>");
                            }
                        }
                        offerTimer();
                        AsOfferCounter = setInterval(function () { offerTimer() }, 1000);
                    }
                    else {
                        self.$target.find('#as_product_offer').empty();
                    }
                }
                else {
                    self.$target.find('#as_product_offer').empty();
                }
            })

        } catch (error) {}
        if (combination['has_discounted_price']) {
            var $discount = $('#product_discount_percent')
            $discount.text('(' + String(100 - Math.round((combination['price'] * 100)/combination['list_price'])) + '%' + ') OFF');
        }
        else{
            var $discount = $('#product_discount_percent')
            $discount.empty();
        }
    }
    else {
        if(self.$target != undefined){
            self.$target.find('#as_product_offer').empty();
        }
    }
    combinationVariant.apply(this, [ev, $parent, combination]);
};

publicWidget.registry.as_youtube_popup = publicWidget.Widget.extend({
    selector: "#wrapwrap",
    'events':{
        'click .popup-youtube':'_openVideoPop'
    },
    _openVideoPop:function(ev){
        ev.preventDefault();
        $(ev.currentTarget).magnificPopup({
            disableOn: 700,
            type: 'iframe',
            mainClass: 'mfp-fade',
            removalDelay: 160,
            preloader: false,
            fixedContentPos: false
        });
    },
})

});