odoo.define('theme_alan.catProductDialog', function (require) {
"use strict";

const webEditor = require('web_editor.widget');
const webUtils = require('web.utils');
const options = require('web_editor.snippets.options');
const { BaseAlanQweb, FetchProductsData, FetchCategoryData} = require("theme_alan.core_mixins");
const catProductDialog = webEditor.Dialog;
const webCore = require('web.core');
const _t = webCore._t;
const recordSelector = require('theme_alan.recordSelector')

let baseProduct = catProductDialog.extend(FetchProductsData, FetchCategoryData, BaseAlanQweb,{
    template: 'theme_alan.core_dialog',
    xmlDependencies: catProductDialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_dialog.xml',
        '/theme_alan/static/src/xml/snippets/categ_product_dialog.xml',
        '/theme_alan/static/src/xml/snippets/base_templates.xml' ]),
    events: _.extend({}, catProductDialog.prototype.events, {
        'click .as-save-dialog': '_onSavebtn',
        'click .as-close-dialog': 'close',
        'click .as-record-rm-btn': '_removeRecDiv',
        'click .as-add-prod-btn': '_openProductDialog',
        'click #add-btn-cat': '_openCatDialog',
        'click .autoSlider': '_sliderTimer',
        'click .pre_select': '_selectLayout',
    }),

    willStart: function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            if(cr.opts.initRecords != "") {
                cr._fetchProductRawData(cr.opts.initRecords, "product.template").then(function(rec){
                    cr._initData("Product", rec);
                });
            }
            if(cr.opts.catRecords != "") {
                cr._fetchCategoryRawData(cr.opts.catRecords).then(function(rec){
                    cr._initData("Category", rec);
                });
            }
        });
    },

    _initData: function(popupType, rec){
        var cr = this;
        var opts = this.opts;
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
        if (popupType == "Category") {
            var catBtn = cr.$el.find("#add-btn-cat");
            catBtn.remove();
            var alertMsg = cr.$el.find(".alertMsg");
            alertMsg.removeClass('d-none');
            const CatTemp = cr._baseAlanQweb("theme_alan.dialog_catProd_list_view_init",rec);
            let $mainDataDiv = cr.$el.find(".as-cat-select-list-view");
            $mainDataDiv.empty().append(CatTemp);
            $mainDataDiv.find(".as-sort-data").sortable();
        }
        let style_id = "#"+opts.styleUI;
        let autoSlider = "#"+opts.autoSlider;
        let sTimer = "#sec"+opts.sTimer;
        let cart = "#"+opts.cart;
        let quickView = "#"+opts.quickView;
        let compare = "#"+opts.compare;
        let wishList = "#"+opts.wishList;
        let prodLabel = "#"+opts.prodLabel;
        let rating = "#"+opts.rating;
        let infinity = "#"+opts.infinity;
        let slider_id = opts.slider;
        cr.$el.find(style_id).prop("checked","checked");
        if (autoSlider == "#") {
            cr.$el.find("input[name='autoSlider']").prop("checked", false);
            cr.$el.find(".infinity_option").addClass('d-none');
        } else {
            cr.$el.find(autoSlider).prop("checked","checked");
            cr.$el.find(".timerClass").removeClass('d-none');
            cr.$el.find(".infinity_option").removeClass('d-none');
            cr.$el.find(sTimer).prop("checked","checked");
            infinity == "#" ? cr.$el.find("#infinity").prop("checked", false) : cr.$el.find("#infinity").prop("checked", "checked");
        }
        cart == "#" ? cr.$el.find("#cart").prop("checked", false) : cr.$el.find("#cart").prop("checked", "checked");
        quickView == "#" ? cr.$el.find("#quickView").prop("checked", false) : cr.$el.find("#quickView").prop("checked", "checked");
        compare == "#" ? cr.$el.find("#compare").prop("checked", false) : cr.$el.find("#compare").prop("checked", "checked");
        wishList == "#" ? cr.$el.find("#wishList").prop("checked", false) : cr.$el.find("#wishList").prop("checked", "checked");
        prodLabel == "#" ? cr.$el.find("#prodLabel").prop("checked", false) : cr.$el.find("#prodLabel").prop("checked", "checked");
        rating == "#" ? cr.$el.find("#rating").prop("checked", false) : cr.$el.find("#rating").prop("checked", "checked");

        cr.$el.find(".dataPreview").addClass('d-none');
        var sPreview = ".s"+style_id.slice(-1);
        cr.$el.find(sPreview).removeClass('d-none');
        cr.$el.find(".imgPreview").addClass('d-none');
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

    _catDataFetch(){
        let cr = this;
        let $selectedCat = cr.$el.find(".as-cat-select-list-view");
        let initDataDic = [];
        let initIds = [];
        $selectedCat.find(".as-record-card-view").each(function (ind, ele) {
            initDataDic.push({'id': $(ele).data("catId"),'text': $(ele).data("catName") })
            initIds.push($(ele).data("catId"));
        });
        return [initDataDic,initIds];
    },

    _openProductDialog: function(ev) {
        let cr = this;
        let perent_id = $(ev.currentTarget).data("catId");
        let prePosData = cr._prodDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Product'),
            coreTitle:_t('Product Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'CategProd',
            extraData:prePosData[2],
            parentDomain:perent_id,
            customTemplate:'theme_alan.as_select2_products_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
    },

    _openCatDialog: function(ev) {
        let cr = this;
        let prePosData = cr._catDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Category'),
            coreTitle:_t('Category Configuration'),
            route:"/get/select2/data",
            isMultiSelect:false,
            initData:prePosData[0][0],
            initIds:prePosData[1],
            searchType:'CatProds',
            customTemplate:'theme_alan.as_select2_category_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
    },

    _sliderTimer: function(ev) {
        if(this.$el.find('.autoSlider').is(":checked")) {
            this.$el.find(".timerClass").removeClass('d-none');
            this.$el.find(".infinity_option").removeClass('d-none');
        }
        else {
            this.$el.find(".timerClass").addClass('d-none');
            this.$el.find(".infinity_option").addClass('d-none');
        }
    },

    _selectLayout: function(ev) {
        this.$el.find(".dataPreview").addClass('d-none');
        var layout_style = this.$el.find("input[name='layoutStyle']:checked").val();
        var sPreview = ".s"+layout_style.slice(-1);
        this.$el.find(sPreview).removeClass('d-none');
    },

    _removeRecDiv: function(ev) {
        $(ev.currentTarget).parents(".as-record-card-view").remove();
    },

    _onSavebtn: function(ev) {
        var cr = this;
        let prePosData = cr._prodDataFetch();
        let prodIds = JSON.stringify(prePosData[1]);
        cr.src.$target.attr("data-prod-ids", prodIds);
        let prePostData = cr._catDataFetch();
        let catIds = JSON.stringify(prePostData[1]);
        cr.src.$target.attr("data-cat-ids", catIds);
        let styleUI = cr.$el.find("input[name='layoutStyle']:checked").val();
        let autoSlider = cr.$el.find("input[name='autoSlider']:checked").val();
        let cart = cr.$el.find("input[name='cart']:checked").val();
        let quickView = cr.$el.find("input[name='quickView']:checked").val();
        let compare = cr.$el.find("input[name='compare']:checked").val();
        let wishList = cr.$el.find("input[name='wishList']:checked").val();
        let prodLabel = cr.$el.find("input[name='prodLabel']:checked").val();
        let rating = cr.$el.find("input[name='rating']:checked").val();
        let infinity = cr.$el.find("input[name='infinity']:checked").val();
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
        cr.src.$target.attr("data-styleUI", styleUI);
        cr.src.$target.attr("data-autoSlider", autoSliders);
        cr.src.$target.attr("data-cart", carts);
        cr.src.$target.attr("data-quickView", quickViews);
        cr.src.$target.attr("data-compare", compares);
        cr.src.$target.attr("data-wishList", wishLists);
        cr.src.$target.attr("data-prodLabel", prodLabels);
        cr.src.$target.attr("data-rating", ratings);
        cr.src.$target.attr("data-infinity", infinitys);
        cr.src.$target.attr("data-slider", sliderType);
        cr.$el.find(".as-close-dialog").trigger('click');
    },
});
return baseProduct
});