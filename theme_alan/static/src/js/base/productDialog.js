odoo.define('theme_alan.productDialog', function (require) {
"use strict";

const webEditor = require('web_editor.widget');
const webUtils = require('web.utils');
const options = require('web_editor.snippets.options');
const { BaseAlanQweb, FetchProductsData } = require("theme_alan.core_mixins");
const productDialog = webEditor.Dialog;
const webCore = require('web.core');
const _t = webCore._t;
const recordSelector = require('theme_alan.recordSelector')

let baseProduct = productDialog.extend(FetchProductsData, BaseAlanQweb,{
    template: 'theme_alan.core_dialog',
    xmlDependencies: productDialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_dialog.xml',
        '/theme_alan/static/src/xml/snippets/product_dialog.xml',
        '/theme_alan/static/src/xml/snippets/product_banner_dialog.xml',
        '/theme_alan/static/src/xml/snippets/product_offer_dialog.xml',
        '/theme_alan/static/src/xml/snippets/base_templates.xml' ]),
    events: _.extend({}, productDialog.prototype.events, {
        'click .as-save-dialog': '_onSavebtn',
        'click .as-save-timer': '_onSavetime',
        'click .as-close-dialog': 'close',
        'click .as-record-rm-btn': '_removeRecDiv',
        'click #add-btn-product': '_openProductDialog',
        'click #add-btn-prod_variant': '_openProdVariantDialog',
        'click #add-btn-product-offer': '_openProductOfferDialog',
        'click .autoSlider': '_sliderTimer',
        'click .pre_select': '_selectLayout',
        'click .sel_position': '_selectPosition',
        'click .ui_option': '_showSliderOption',
        'change .prod-count': '_changeProdCount',
    }),

    willStart: function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            if(cr.opts.popupType == "Product" || cr.opts.popupType == "Product Banner" || cr.opts.popupType == "Product Offer") {
                if(cr.opts.initRecords != "") {
                    cr._fetchProductRawData(cr.opts.initRecords, "product.template").then(function(rec){
                        cr._initData("Product", rec);
                    });
                }
            } else if(cr.opts.popupType == "Product Variant") {
                if(cr.opts.initRecords != "") {
                    cr._fetchProductRawData(cr.opts.initRecords, "product.product").then(function(rec){
                        cr._initData("Product", rec);
                    });
                }
            } else if(cr.opts.popupType == "Best Product") {
                 cr._fetchProductRawData([], "product.product").then(function(rec){
                        cr._initData("Best Product", rec);
                });
            } else if(cr.opts.popupType == "Latest Product") {
                 cr._fetchProductRawData([], "product.product").then(function(rec){
                        cr._initData("Latest Product", rec);
                });
            } else if(cr.opts.popupType == "Offer Banner"){
                cr._fetchProductRawData([], "product.product").then(function(rec){
                    cr._initData("Offer Banner", rec);
                });
            } else if(cr.opts.popupType == "Offer"){
                cr._fetchProductRawData([], "product.product").then(function(rec){
                    cr._initData("Offer", rec);
                });
            }
        });
    },

    _initData: function(popupType, rec){
        var cr = this;
        var opts = this.opts;
        if(popupType == "Offer") {
            var offerTime = opts.TimerData;
            cr.$el.find("input[name='offerTime']").val(offerTime);
        }
        if (popupType == "Product") {
            let clean_res = []
            if (rec != undefined) {
                for (const r of rec) {
                    r['price'] = webUtils.Markup(r['price']);
                    clean_res.push(r);
                }
            }
            const ProdTemp = cr._baseAlanQweb("theme_alan.dialog_product_list_view_init",clean_res);
            let $mainDataDiv = cr.$el.find(".as-product-select-list-view");
            $mainDataDiv.empty().append(ProdTemp);
            $mainDataDiv.find(".as-sort-data").sortable();
        }
        if(popupType  == "Offer Banner"){
            let offerTime = opts.offerTime;
            cr.$el.find("input[name='offerTime']").val(offerTime);
        }
        else if (popupType != "Offer"){
            let ui_id = "#"+opts.mainUI;
            let imgPosition = "#"+opts.imgPosition;
            let offerTime = opts.offerTime;
            let style_id = "#"+opts.styleUI;
            let autoSlider = "#"+opts.autoSlider;
            let dataCount = "#val"+opts.dataCount;
            let sTimer = "#sec"+opts.sTimer;
            let cart = "#"+opts.cart;
            let buyNow = "#"+opts.buyNow;
            let totalCount = opts.totalCount;
            let quickView = "#"+opts.quickView;
            let compare = "#"+opts.compare;
            let wishList = "#"+opts.wishList;
            let prodLabel = "#"+opts.prodLabel;
            let rating = "#"+opts.rating;
            let infinity = "#"+opts.infinity;
            let slider_id = opts.slider;
            cr.$el.find(ui_id).prop("checked","checked");
            cr.$el.find(imgPosition).prop("checked","checked");
            cr.$el.find("input[name='totalCount']").val(totalCount);
            cr.$el.find("input[name='offerTime']").val(offerTime);
            cr.$el.find(style_id).prop("checked","checked");
            if(cr.$el.find("input[name='snippetView']:checked").val() == "slider") {
                cr.$el.find(".sl_option").removeClass('d-none');
            }
            else {
                cr.$el.find(".sl_option").addClass('d-none');
            }
            if (autoSlider == "#") {
                cr.$el.find("input[name='autoSlider']").prop("checked", false);
                cr.$el.find(".slider_loop").addClass('d-none');
            } else {
                cr.$el.find(autoSlider).prop("checked","checked");
                cr.$el.find(".timerClass").removeClass('d-none');
                cr.$el.find(".slider_loop").removeClass('d-none');
                if(cr.$el.find("input[name='snippetView']:checked").val() == "slider") {
                    cr.$el.find(".infinity_option").removeClass('d-none');
                }
                cr.$el.find(sTimer).prop("checked","checked");
                infinity == "#" ? cr.$el.find("#infinity").prop("checked", false) : cr.$el.find("#infinity").prop("checked", "checked");
            }
            cart == "#" ? cr.$el.find("#cart").prop("checked", false) : cr.$el.find("#cart").prop("checked", "checked");
            buyNow == "#" ? cr.$el.find("#buyNow").prop("checked", false) : cr.$el.find("#buyNow").prop("checked", "checked");
            quickView == "#" ? cr.$el.find("#quickView").prop("checked", false) : cr.$el.find("#quickView").prop("checked", "checked");
            compare == "#" ? cr.$el.find("#compare").prop("checked", false) : cr.$el.find("#compare").prop("checked", "checked");
            wishList == "#" ? cr.$el.find("#wishList").prop("checked", false) : cr.$el.find("#wishList").prop("checked", "checked");
            prodLabel == "#" ? cr.$el.find("#prodLabel").prop("checked", false) : cr.$el.find("#prodLabel").prop("checked", "checked");
            rating == "#" ? cr.$el.find("#rating").prop("checked", false) : cr.$el.find("#rating").prop("checked", "checked");

            cr.$el.find(dataCount).prop("checked","checked");
            cr.$el.find(".dataPreview").addClass('d-none');
            var sPreview = "."+ui_id[1]+style_id.slice(-1);
            cr.$el.find(sPreview).removeClass('d-none');
            cr.$el.find(".imgPreview").addClass('d-none');
            var img_preview = cr.$el.find(imgPosition).prop("checked","checked").val();
            cr.$el.find("."+img_preview).removeClass('d-none');
            cr.$el.find("#slider_pagination").val(slider_id);
        }
    },
    start:function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            cr.$modal.find('.modal-content').addClass('as-full-modal');
        })
    },
    init: function (src, opts) {
        let cr = this;
        cr._super(src, _.extend({ fullSubTemplate: opts.fullSubTemplate || 0,
            enableCoreButton: opts.enableCoreButton,enableCoreTitle: opts.enableCoreTitle,
            subTemplate: opts.subTemplate || "",
            coreTitle: opts.coreTitle || _t('Configuration'),
            size: opts.size || 'extra-large',
            renderHeader: 0, renderFooter: 0 }));
        cr.src = src;
        cr.opts = opts;
    },

    _prodDataFetch(){
        let cr = this;
        let $selectedProduct = cr.$el.find(".as-product-select-list-view");
        let initDataDic = [];
        let initIds = [];
        $selectedProduct.find(".as-record-card-view").each(function (ind, ele) {
            initDataDic.push({'id': $(ele).data("prodId"),'text': $(ele).data("prodName") })
            initIds.push($(ele).data("prodId"));
        });
        return [initDataDic,initIds];
    },

    _openProductDialog: function(ev) {
        let cr = this;
        let prePosData = cr._prodDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Product'),
            coreTitle:_t('Product Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'Product',
            customTemplate:'theme_alan.as_select2_products_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
    },

    _openProductOfferDialog: function(ev) {
        let cr = this;
        let prePosData = cr._prodDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Product'),
            coreTitle:_t('Product Configuration'),
            route:"/get/select2/data",
            isMultiSelect:false,
            initData:prePosData[0][0],
            initIds:prePosData[1],
            searchType:'Product',
            customTemplate:'theme_alan.as_select2_products_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
    },

    _openProdVariantDialog: function(ev) {
        let cr = this;
        let prePosData = cr._prodDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Product Variant'),
            coreTitle:_t('Product Variant Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'Product Variant',
            customTemplate:'theme_alan.as_select2_products_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
    },

    _sliderTimer: function(ev) {
        if(this.$el.find('.autoSlider').is(":checked")) {
            this.$el.find(".timerClass").removeClass('d-none');
            this.$el.find(".slider_loop").removeClass('d-none');
            if(this.$el.find("input[name='snippetView']:checked").val() == "slider") {
                this.$el.find(".infinity_option").removeClass('d-none');
            }
        }
        else {
            this.$el.find(".timerClass").addClass('d-none');
            this.$el.find(".infinity_option").addClass('d-none');
            this.$el.find(".slider_loop").addClass('d-none');
        }
    },

    _showSliderOption: function(ev) {
        if(this.$el.find("input[name='snippetView']:checked").val() == "slider") {
            this.$el.find(".sl_option").removeClass('d-none');
            if(this.$el.find('.autoSlider').is(":checked")){
                this.$el.find(".infinity_option").removeClass('d-none');
            }
        }
        else {
            this.$el.find(".sl_option").addClass('d-none');
            this.$el.find(".infinity_option").addClass('d-none');
        }
    },

    _changeProdCount: function(ev){
        var prodCount = this.$el.find("input[name='totalCount']").val();
        if (prodCount < 1){
            this.$el.find("input[name='totalCount']").val(1);
        }
    },

    _selectLayout: function(ev) {
        this.$el.find(".dataPreview").addClass('d-none');
        var mainView = this.$el.find("input[name='snippetView']:checked").val();
        var layout_style = this.$el.find("input[name='layoutStyle']:checked").val();
        var sPreview = "."+mainView[0]+layout_style.slice(-1);
        this.$el.find(sPreview).removeClass('d-none');
    },

    _selectPosition: function(ev) {
        this.$el.find(".imgPreview").addClass('d-none');
        var mainPosition = this.$el.find("input[name='imgPosition']:checked").val();
        this.$el.find("."+mainPosition).removeClass('d-none');
    },

    _removeRecDiv: function(ev) {
        $(ev.currentTarget).parents(".as-record-card-view").remove();
    },

    _onSavebtn: function(ev) {
        var cr = this;
        if (cr.src.data.selector == ".as_product_slider" || cr.src.data.selector == ".as_product_variant_slider" || cr.src.data.selector == ".as_product_banner_slider" || cr.src.data.selector == ".as_product_offer") {
            let prePosData = cr._prodDataFetch();
            let prodIds = JSON.stringify(prePosData[1]);
            cr.src.$target.attr("data-prod-ids", prodIds);
        }
        let mainUI = cr.$el.find("input[name='snippetView']:checked").val();
        let imgPosition = cr.$el.find("input[name='imgPosition']:checked").val();
        let offerTime = cr.$el.find("input[name='offerTime']").val();
        let styleUI = cr.$el.find("input[name='layoutStyle']:checked").val();
        let autoSlider = cr.$el.find("input[name='autoSlider']:checked").val();
        let cart = cr.$el.find("input[name='cart']:checked").val();
        let quickView = cr.$el.find("input[name='quickView']:checked").val();
        let compare = cr.$el.find("input[name='compare']:checked").val();
        let buyNow = cr.$el.find("input[name='buyNow']:checked").val();
        let wishList = cr.$el.find("input[name='wishList']:checked").val();
        let prodLabel = cr.$el.find("input[name='prodLabel']:checked").val();
        let rating = cr.$el.find("input[name='rating']:checked").val();
        let infinity = cr.$el.find("input[name='infinity']:checked").val();
        var dataCount = cr.$el.find("input[name='dataCount']:checked").val();
        var totalCount = cr.$el.find("input[name='totalCount']").val();
        var sliderType = cr.$el.find("#slider_pagination").val();
        if (autoSlider != undefined) {
            var sTimer = cr.$el.find("input[name='sTimer']:checked").val();
            cr.src.$target.attr("data-sTimer", sTimer);
        }
        var autoSliders = autoSlider == undefined? "":autoSlider;
        var carts = cart == undefined? "":cart;
        var buyNows = buyNow == undefined? "":buyNow;
        var quickViews = quickView == undefined? "":quickView;
        var compares = compare == undefined? "":compare;
        var wishLists = wishList == undefined? "":wishList;
        var prodLabels = prodLabel == undefined? "":prodLabel;
        var ratings = rating == undefined? "":rating;
        var infinitys = infinity == undefined? "":infinity;
        cr.src.$target.attr("data-mainUI", mainUI);
        cr.src.$target.attr("data-styleUI", styleUI);
        cr.src.$target.attr("data-offerTime", offerTime);
        cr.src.$target.attr("data-imgPosition", imgPosition);
        cr.src.$target.attr("data-autoSlider", autoSliders);
        cr.src.$target.attr("data-cart", carts);
        cr.src.$target.attr("data-buyNow", buyNows);
        cr.src.$target.attr("data-quickView", quickViews);
        cr.src.$target.attr("data-compare", compares);
        cr.src.$target.attr("data-wishList", wishLists);
        cr.src.$target.attr("data-prodLabel", prodLabels);
        cr.src.$target.attr("data-rating", ratings);
        cr.src.$target.attr("data-infinity", infinitys);
        cr.src.$target.attr("data-dataCount", dataCount);
        cr.src.$target.attr("data-totalCount", totalCount);
        cr.src.$target.attr("data-slider", sliderType);
        cr.$el.find(".as-close-dialog").trigger('click');
    },

    _onSavetime: function(ev) {
        var cr = this;
        var perent_id = cr.$el.find("#perent_id").val();
        var offerTime = cr.$el.find("#offerTime").val();
        cr.src.$el.find(".as-record-card-view[data-prod-id='"+perent_id+"']").attr('data-time-data', offerTime);
        cr.$el.find(".as-close-dialog").trigger('click');
    },
});
return baseProduct
});