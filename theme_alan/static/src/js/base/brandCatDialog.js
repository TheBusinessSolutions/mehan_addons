odoo.define('theme_alan.brandCatDialog', function (require) {
"use strict";

const webEditor = require('web_editor.widget');
const weWidgets = require('wysiwyg.widgets');
const webUtils = require('web.utils');
const options = require('web_editor.snippets.options');
const { BaseAlanQweb, FetchCategoryData, FetchBrandData, FetchBlogData } = require("theme_alan.core_mixins");
const brandCatDialog = webEditor.Dialog;
const webCore = require('web.core');
const _t = webCore._t;
const recordSelector = require('theme_alan.recordSelector')

let baseBrandCat = brandCatDialog.extend(FetchBrandData, FetchBlogData, FetchCategoryData, BaseAlanQweb,{
    template: 'theme_alan.core_dialog',
    xmlDependencies: brandCatDialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_dialog.xml',
        '/theme_alan/static/src/xml/record_list_view.xml',
        '/theme_alan/static/src/xml/snippets/cat_brand_dialog.xml',
        '/theme_alan/static/src/xml/snippets/base_templates.xml' ]),
    events: _.extend({}, brandCatDialog.prototype.events, {
        'click .as-save-dialog': '_onSavebtn',
        'click .as-close-dialog': 'close',
        'click .as-rec-rm-btn': '_removeRecDiv',
        'click #add-btn-brand': '_openBrandDialog',
        'click #add-btn-cat': '_openCatDialog',
        'click #add-btn-blog': '_openBlogDialog',
        'click .autoSlider': '_sliderTimer',
        'click .pre_select': '_selectLayout',
        'click .ui_option': '_showSliderOption',
        'click .add_image': '_addImagesToGallery',
        'click #add-btn-tab': '_addTabs',
        'click .as-save-tab-dialog': '_saveTabDialog',
        'click #remove-tab': '_removeTab',
        'click .as-img-remove': '_imgRemoveBtn',
    }),

    willStart: function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            if(cr.opts.popupType == "Brand") {
                if(cr.opts.initRecords != "") {
                    cr._fetchBrandRawData(cr.opts.initRecords).then(function(rec){
                        cr._initData(rec, "Brand");
                    });
                }
            }
            else if(cr.opts.popupType == "Category") {
                if(cr.opts.initRecords != "") {
                    cr._fetchCategoryRawData(cr.opts.initRecords).then(function(rec){
                        cr._initData(rec, "Category");
                    });
                }
            }
            else if(cr.opts.popupType == "Blog") {
                if(cr.opts.initRecords != "") {
                    cr._fetchBlogRawData(cr.opts.initRecords).then(function(rec){
                        cr._initData(rec, "Blog");
                    });
                }
            }
            else if(cr.opts.popupType == "tabImage") {
                if(cr.opts.tabData != "") {
                    cr._fetchBlogRawData([]).then(function(rec){
                        cr._initData(cr.opts.tabData, "tabImage");
                    });
                }
            }
        });
    },

    _initData: function(rec, popupType){
        var cr = this;
        var opts = this.opts;
        if (cr.opts.popupType == "tabImage"){
            var data = JSON.parse(rec);
            const TabTemp = cr._baseAlanQweb("theme_alan.dialog_add_tab_view_init",data);
            let $mainDataDiv = cr.$el.find(".as-tab-select-list-view");
            $mainDataDiv.empty().append(TabTemp);
            $mainDataDiv.sortable();
            cr.$el.find('.container').sortable();
        } else {
            if (cr.opts.popupType == "Brand") {
                const BrandTemp = cr._baseAlanQweb("theme_alan.dialog_brand_list_view_init",rec);
                let $mainDataDiv = cr.$el.find(".as-brand-select-list-view");
                $mainDataDiv.empty().append(BrandTemp);
                $mainDataDiv.find(".as-sort-data").sortable();
            } else if (cr.opts.popupType == "Category") {
                const CatTemp = cr._baseAlanQweb("theme_alan.dialog_categ_list_view_init",rec);
                let $mainDataDiv = cr.$el.find(".as-cat-select-list-view");
                $mainDataDiv.empty().append(CatTemp);
                $mainDataDiv.find(".as-sort-data").sortable();
            } else if (cr.opts.popupType == "Blog") {
                const BlogTemp = cr._baseAlanQweb("theme_alan.dialog_blog_list_view_init",rec);
                let $mainDataDiv = cr.$el.find(".as-blog-select-list-view");
                $mainDataDiv.empty().append(BlogTemp);
                $mainDataDiv.find(".as-sort-data").sortable();
            }
            let ui_id = "#"+opts.mainUI;
            let tab_option = "#"+opts.tabOption;
            let style_id = "#"+opts.styleUI;
            let recordLink = "#"+opts.recordLink;
            let recordName = "#"+opts.recordName;
            let autoSlider = "#"+opts.autoSlider;
            let dataCount = "#val"+opts.dataCount;
            let sTimer = "#sec"+opts.sTimer;
            let buyNow = "#"+opts.buyNow;
            let cart = "#"+opts.cart;
            let quickView = "#"+opts.quickView;
            let compare = "#"+opts.compare;
            let wishList = "#"+opts.wishList;
            let prodLabel = "#"+opts.prodLabel;
            let rating = "#"+opts.rating;
            let infinity = "#"+opts.infinity;
            let slider_id = opts.slider;
            cr.$el.find(ui_id).prop("checked","checked");
            cr.$el.find(tab_option).prop("checked","checked");
            cr.$el.find(style_id).prop("checked","checked");
            if(cr.$el.find("input[name='snippetView']:checked").val() == "slider") {
                cr.$el.find(".sl_option").removeClass('d-none');
            }
            else {
                cr.$el.find(".sl_option").addClass('d-none');
            }
            if (recordLink == "#"){
                cr.$el.find("input[name='recordLink']").prop("checked", false);
            }
            if (recordName == "#"){
                cr.$el.find("input[name='recordName']").prop("checked", false);
            }
            if (autoSlider == "#") {
                cr.$el.find("input[name='autoSlider']").prop("checked", false);
            } else {
                cr.$el.find(autoSlider).prop("checked","checked");
                cr.$el.find(".timerClass").removeClass('d-none');
                cr.$el.find(sTimer).prop("checked","checked");
                if(cr.$el.find("input[name='snippetView']:checked").val() == "slider") {
                    cr.$el.find(".infinity_option").removeClass('d-none');
                }
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
            cr.$el.find("#slider_pagination").val(slider_id);
        }
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

    start:function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            cr.$modal.find('.modal-content').addClass('as-full-modal');
        })
    },

    _addTabs: function(){
        var cr = this;
        var $mainDataDiv = cr.$el.find('.as-tab-select-list-view');
        const ProdTemp = cr._baseAlanQweb("theme_alan.dialog_add_tab_view", {});
        $mainDataDiv.append(ProdTemp);
        $mainDataDiv.sortable();
    },

    _addImagesToGallery: function(ev){
        var $container = $(ev.currentTarget).parents().closest('.as-sort-data').find('.container');
        $container.sortable();
        const $images = $container.find('img');
        var dialog = new weWidgets.MediaDialog(this, {multiImages: true, onlyImages: true, mediaWidth: 1920});
        return new Promise(resolve => {
            dialog.on('save', this, function (attachments) {
                for (var i = 0; i < attachments.length; i++) {
                    var $rm_btn = $('<div class="as-img-div"><span class="as-img-remove"/></div>');
                    $('<img/>', {
                        class: $images.length > 0 ? $images[0].className : 'as-img-gallery ',
                        src: attachments[i].image_src,
                        alt: attachments[i].description || '',
                        'data-name': _t('Image'),
                        style: $images.length > 0 ? $images[0].style.cssText : '',
                    }).appendTo($rm_btn);
                    $rm_btn.appendTo($container);
                }
            });
            dialog.on('closed', this, () => resolve());
            dialog.open();
        });
    },

    _imgRemoveBtn: function(ev){
        $(ev.currentTarget).parent().remove();
    },

    _brandDataFetch(){
        let cr = this;
        let $selectedBrand = cr.$el.find(".as-brand-select-list-view");
        let initDataDic = [];
        let initIds = [];
        $selectedBrand.find(".as-record-card-view").each(function (ind, ele) {
            initDataDic.push({'id': $(ele).data("brandId"),'text': $(ele).data("brandName") })
            initIds.push($(ele).data("brandId"));
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

    _blogDataFetch(){
        let cr = this;
        let $selectedBlog = cr.$el.find(".as-blog-select-list-view");
        let initDataDic = [];
        let initIds = [];
        $selectedBlog.find(".as-record-card-view").each(function (ind, ele) {
            initDataDic.push({'id': $(ele).data("blogId"),'text': $(ele).data("blogName") })
            initIds.push($(ele).data("blogId"));
        });
        return [initDataDic,initIds];
    },

    _openBrandDialog: function(ev) {
        let cr = this;
        let prePosData = cr._brandDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Brand'),
            coreTitle:_t('Brand Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'BrandMix',
            customTemplate:'theme_alan.as_select2_brand_dropdown'};
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
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'CatMix',
            extraData:[],
            parentDomain:false,
            customTemplate:'theme_alan.as_select2_category_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
    },

    _openBlogDialog: function(ev) {
        let cr = this;
        let prePosData = cr._blogDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Blog'),
            coreTitle:_t('Blog Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'Blogs',
            extraData:[],
            parentDomain:false,
            customTemplate:'theme_alan.as_select2_blog_dropdown'};
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

    _selectLayout: function(ev) {
        this.$el.find(".dataPreview").addClass('d-none');
        var mainView = this.$el.find("input[name='snippetView']:checked").val();
        var layout_style = this.$el.find("input[name='layoutStyle']:checked").val();
        var sPreview = "."+mainView[0]+layout_style.slice(-1);
        this.$el.find(sPreview).removeClass('d-none');
    },

    _removeRecDiv: function(ev) {
        $(ev.currentTarget).parents(".as-record-card-view").remove();
    },
    
    _removeTab: function(ev){
        $(ev.currentTarget).parents().closest('.as-sort-data').remove();
    },

    _saveTabDialog: function(){
        var cr = this;
        var tab_data = {};
        var $tabDiv = cr.$el.find('.as-sort-data');
        $.each($tabDiv, function(ind, val){
            var tabTitle = $(val).find("input[name='tabTitle']").val();
            var $tabImages = $(val).find(".container").find('img');
            var imgs = [];
            $.each($tabImages, function(ind, img){
                var src = $(img).attr('src');
                imgs.push(src);
            });
            tab_data[tabTitle] = imgs;
        });
        cr.src.$target.attr("data-tabData", JSON.stringify(tab_data));
        cr.$el.find(".as-close-dialog").trigger('click');
    },

    _onSavebtn: function(ev) {
        var cr = this;
        if (cr.src.data.selector == ".as_brand_slider" || cr.src.data.selector == ".as_brand_product_slider") {
            let prePosData = cr._brandDataFetch();
            let brandIds = JSON.stringify(prePosData[1]);
            cr.src.$target.attr("data-brand-ids", brandIds);
        }
        else if (cr.src.data.selector == ".as_cat_slider" || cr.src.data.selector == ".as_cat_product_slider") {
            let prePosData = cr._catDataFetch();
            let catIds = JSON.stringify(prePosData[1]);
            cr.src.$target.attr("data-cat-ids", catIds);
        }
        else if (cr.src.data.selector == ".as_blog_slider") {
            let prePosData = cr._blogDataFetch();
            let blogIds = JSON.stringify(prePosData[1]);
            cr.src.$target.attr("data-blog-ids", blogIds);
        }

        let tabOption = cr.$el.find("input[name='tabOptions']:checked").val();
        let mainUI = cr.$el.find("input[name='snippetView']:checked").val();
        let styleUI = cr.$el.find("input[name='layoutStyle']:checked").val();
        let recordLink = cr.$el.find("input[name='recordLink']:checked").val();
        let recordName = cr.$el.find("input[name='recordName']:checked").val();
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
        var sliderType = cr.$el.find("#slider_pagination").val();
        if (autoSlider != undefined) {
            var sTimer = cr.$el.find("input[name='sTimer']:checked").val();
            cr.src.$target.attr("data-sTimer", sTimer);
        }
        var recordLinks = recordLink == undefined? "":recordLink;
        var recordNames = recordName == undefined? "":recordName;
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
        cr.src.$target.attr("data-tabOption", tabOption);
        cr.src.$target.attr("data-recordLink", recordLinks);
        cr.src.$target.attr("data-recordName", recordNames);
        cr.src.$target.attr("data-autoSlider", autoSliders);
        cr.src.$target.attr("data-dataCount", dataCount);
        cr.src.$target.attr("data-cart", carts);
        cr.src.$target.attr("data-buyNow", buyNows);
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
return baseBrandCat
});