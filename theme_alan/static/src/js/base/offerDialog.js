odoo.define('theme_alan.offerDialog', function (require) {
"use strict";

const webEditor = require('web_editor.widget');
const webUtils = require('web.utils');
const options = require('web_editor.snippets.options');
const { BaseAlanQweb, FetchProductsData} = require("theme_alan.core_mixins");
const offerDialog = webEditor.Dialog;
const productDialog = require('theme_alan.productDialog');
const webCore = require('web.core');
const _t = webCore._t;
const recordSelector = require('theme_alan.recordSelector')

let baseProduct = offerDialog.extend(FetchProductsData, BaseAlanQweb,{
    template: 'theme_alan.core_dialog',
    xmlDependencies: offerDialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_dialog.xml',
        '/theme_alan/static/src/xml/snippets/offer_slider_dialog.xml',
        '/theme_alan/static/src/xml/snippets/base_templates.xml' ]),
    events: _.extend({}, offerDialog.prototype.events, {
        'click .as-save-dialog': '_onSavebtn',
        'click .as-close-dialog': 'close',
        'click .as-record-rm-btn': '_removeRecDiv',
        'click #as-btn-prodOffer': '_openProdOfferDialog',
        'click .sel_position': '_selectPosition',
        'click .ui_option': '_showSliderOption',
        'click .autoSlider': '_sliderTimer',
        'click .as-add-timer': '_addProdTimer',
    }),

    willStart: function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            if(cr.opts.initRecords != "") {
                if(cr.opts.initRecords.trim() != ""){
                    var initData = JSON.parse(cr.opts.TimerData.replace(/'/g,'"'));
                    cr._fetchProductRawData(cr.opts.initRecords,"product.template").then(function(rec){
                        var clean_res = [];
                        _.each(rec, function (res) {
                            let timeData = initData[res['id']];
                            res['timeData'] =  timeData;
                            clean_res.push(res);
                        });
                        cr._initData(clean_res);
                    });
                }
            }
        });
    },

    _initData: function(rec){
        var cr = this;
        var opts = this.opts;
        const CatTemp = cr._baseAlanQweb("theme_alan.dialog_prod_list_view_init",rec);
        let $mainDataDiv = cr.$el.find(".as-product-select-list-view");
        $mainDataDiv.empty().append(CatTemp);
        $mainDataDiv.find(".as-sort-data").sortable();
        let ui_id = "#"+opts.mainUI;
        let imgPosition = "#"+opts.imgPosition;
        let autoSlider = "#"+opts.autoSlider;
        let dataCount = "#val"+opts.dataCount;
        let sTimer = "#sec"+opts.sTimer;
        let cart = "#"+opts.cart;
        let quickView = "#"+opts.quickView;
        let compare = "#"+opts.compare;
        let wishList = "#"+opts.wishList;
        let prodLabel = "#"+opts.prodLabel;
        let rating = "#"+opts.rating;
        let infinity = "#"+opts.infinity;
        let slider_id = opts.slider;
        cr.$el.find(ui_id).prop("checked","checked");
        cr.$el.find(imgPosition).prop("checked","checked");
        if(cr.$el.find("input[name='snippetView']:checked").val() == "slider") {
            cr.$el.find(".sl_option").removeClass('d-none');
        }
        else {
            cr.$el.find(".sl_option").addClass('d-none');
        }
        if (autoSlider == "#") {
            cr.$el.find("input[name='autoSlider']").prop("checked", false);
        } else {
            cr.$el.find(autoSlider).prop("checked","checked");
            cr.$el.find(".timerClass").removeClass('d-none');
            if(cr.$el.find("input[name='snippetView']:checked").val() == "slider") {
                cr.$el.find(".infinity_option").removeClass('d-none');
            }
            cr.$el.find(sTimer).prop("checked","checked");
            infinity == "#" ? cr.$el.find("#infinity").prop("checked", false) : cr.$el.find("#infinity").prop("checked", "checked");
        }
        cart == "#" ? cr.$el.find("#cart").prop("checked", false) : cr.$el.find("#cart").prop("checked", "checked");
        quickView == "#" ? cr.$el.find("#quickView").prop("checked", false) : cr.$el.find("#quickView").prop("checked", "checked");
        compare == "#" ? cr.$el.find("#compare").prop("checked", false) : cr.$el.find("#compare").prop("checked", "checked");
        wishList == "#" ? cr.$el.find("#wishList").prop("checked", false) : cr.$el.find("#wishList").prop("checked", "checked");
        prodLabel == "#" ? cr.$el.find("#prodLabel").prop("checked", false) : cr.$el.find("#prodLabel").prop("checked", "checked");
        rating == "#" ? cr.$el.find("#rating").prop("checked", false) : cr.$el.find("#rating").prop("checked", "checked");
        
        cr.$el.find(dataCount).prop("checked","checked");
        cr.$el.find(".imgPreview").addClass('d-none');
        var img_preview = cr.$el.find(imgPosition).prop("checked","checked").val();
        cr.$el.find("."+img_preview).removeClass('d-none');
        cr.$el.find("#slider_pagination").val(slider_id);
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

    _timeDataFetch(perent_id){
        let cr = this;
        let $selectedProduct = cr.$el.find(".as-product-select-list-view");
        let $perentDiv = $selectedProduct.find(".as-record-card-view[data-prod-id='"+perent_id+"']");
        if($perentDiv.attr("data-time-data") == undefined){
            return "";
        }
        let initDataDic = $perentDiv.attr("data-time-data");
        return initDataDic;
    },

    _prodDataFetch(){
        let cr = this;
        let $selectedProd = cr.$el.find(".as-product-select-list-view");
        let initDataDic = [];
        let initIds = [];
        let extraData = [];
        $selectedProd.find(".as-record-card-view").each(function (ind, ele) {
            initDataDic.push({'id': $(ele).data("prodId"),'text': $(ele).data("prodName") })
            initIds.push($(ele).data("prodId"));
            extraData.push({'id': $(ele).data("prodId"),
                'timeData': $(ele).data("timeData"),
            })
        });
        return [initDataDic,initIds,extraData];
    },

    _openProdOfferDialog: function(ev) {
        let cr = this;
        let prePosData = cr._prodDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Product'),
            coreTitle:_t('Product Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'ProdOffer',
            parentDomain:false,
            extraData:prePosData[2],
            customTemplate:'theme_alan.as_select2_products_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
    },

    _addProdTimer: function(ev) {
        let cr = this;
        let perent_id = $(ev.currentTarget).data("prodId");
        let prePosData = cr._timeDataFetch(perent_id);
        const OfferData = {
            size:"large",
            subTemplate:webUtils.Markup($(cr._baseAlanQweb("theme_alan.dialog_timer_modal",{'perent_id': perent_id})).html()),
            fullSubTemplate:1,
            enableCoreButton:0,
            enableCoreTitle:0,
            perent_id:perent_id,
            TimerData:prePosData,
            popupType:"Offer",
        }
        cr.productDialog = new productDialog(cr, OfferData);
        cr.productDialog.open();
    },

    _selectPosition: function(ev) {
        this.$el.find(".imgPreview").addClass('d-none');
        var mainPosition = this.$el.find("input[name='imgPosition']:checked").val();
        this.$el.find("."+mainPosition).removeClass('d-none');
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

    _removeRecDiv: function(ev) {
        $(ev.currentTarget).parents(".as-record-card-view").remove();
    },

    _onSavebtn: function(ev) {
        var cr = this;
        let prePosData = cr._prodDataFetch();
        var timeData = {};
        $.each(prePosData[1], function (ind, val) {
            let timer = cr._timeDataFetch(val);
            timeData[val] = timer;
        });
        let prodIds = JSON.stringify(prePosData[1]);
        cr.src.$target.attr("data-prod-ids", prodIds);
        cr.src.$target.attr("data-timerdata", JSON.stringify(timeData));
        let mainUI = cr.$el.find("input[name='snippetView']:checked").val();
        let imgPosition = cr.$el.find("input[name='imgPosition']:checked").val();
        let autoSlider = cr.$el.find("input[name='autoSlider']:checked").val();
        let cart = cr.$el.find("input[name='cart']:checked").val();
        let quickView = cr.$el.find("input[name='quickView']:checked").val();
        let compare = cr.$el.find("input[name='compare']:checked").val();
        let wishList = cr.$el.find("input[name='wishList']:checked").val();
        let prodLabel = cr.$el.find("input[name='prodLabel']:checked").val();
        let rating = cr.$el.find("input[name='rating']:checked").val();
        let infinity = cr.$el.find("input[name='infinity']:checked").val();
        var dataCount = cr.$el.find("input[name='dataCount']:checked").val();
        var sliderType = cr.$el.find("#slider_pagination").val();
        if (autoSlider != undefined) {
            var sTimer = cr.$el.find("input[name='sTimer']:checked").val();
            cr.src.$target.attr("data-sTimer", sTimer);
        }
        var autoSliders = autoSlider == undefined? "":autoSlider;
        var carts = cart == undefined? "":cart;
        var quickViews = quickView == undefined? "":quickView;
        var compares = compare == undefined? "":compare;
        var wishLists = wishList == undefined? "":wishList;
        var prodLabels = prodLabel == undefined? "":prodLabel;
        var ratings = rating == undefined? "":rating;
        var infinitys = infinity == undefined? "":infinity;
        cr.src.$target.attr("data-mainUI", mainUI);
        cr.src.$target.attr("data-imgPosition", imgPosition);
        cr.src.$target.attr("data-autoSlider", autoSliders);
        cr.src.$target.attr("data-cart", carts);
        cr.src.$target.attr("data-quickView", quickViews);
        cr.src.$target.attr("data-compare", compares);
        cr.src.$target.attr("data-wishList", wishLists);
        cr.src.$target.attr("data-prodLabel", prodLabels);
        cr.src.$target.attr("data-rating", ratings);
        cr.src.$target.attr("data-infinity", infinitys);
        cr.src.$target.attr("data-dataCount", dataCount);
        cr.src.$target.attr("data-slider", sliderType);
        cr.src.$target.attr("data-wishList", wishLists);
        cr.$el.find(".as-close-dialog").trigger('click');
    },
});
return baseProduct
});