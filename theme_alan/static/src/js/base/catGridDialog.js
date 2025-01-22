odoo.define('theme_alan.catGridDialog', function (require) {
"use strict";

const webEditor = require('web_editor.widget');
const webUtils = require('web.utils');
const options = require('web_editor.snippets.options');
const { BaseAlanQweb, FetchProductsData, FetchCategoryData} = require("theme_alan.core_mixins");
const catGridDialog = webEditor.Dialog;
const webCore = require('web.core');
const _t = webCore._t;
const recordSelector = require('theme_alan.recordSelector')

let baseProduct = catGridDialog.extend(FetchProductsData, FetchCategoryData, BaseAlanQweb,{
    template: 'theme_alan.core_dialog',
    xmlDependencies: catGridDialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_dialog.xml',
        '/theme_alan/static/src/xml/snippets/category_grid_dialog.xml',
        '/theme_alan/static/src/xml/snippets/base_templates.xml' ]),
    events: _.extend({}, catGridDialog.prototype.events, {
        'click .as-save-dialog': '_onSavebtn',
        'click .as-close-dialog': 'close',
        'click .as-record-rm-btn': '_removeRecDiv',
        'click .as-add-prod-btn': '_openProductDialog',
        'click #add-btn-cat': '_openCatDialog',
        // 'click .autoSlider': '_sliderTimer',
        'click .pre_select': '_selectLayout',
    }),

    willStart: function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            if(cr.opts.initRecords != "") {
                if(cr.opts.initRecords.trim() != ""){
                    var initData = JSON.parse(cr.opts.prodRecords.replace(/'/g,'"'));
                    cr._fetchCategoryRawData(cr.opts.initRecords).then(function(rec){
                        var clean_res = [];
                        _.each(rec, function (res) {
                            let prodData = initData[res['id']];
                            res['prodData'] =  JSON.stringify(prodData[0]);
                            res['prodIds'] = JSON.stringify(prodData[1]);
                            clean_res.push(res);
                        });
                        cr._initData("Category", clean_res);
                    });
                }
            }
        });
    },

    _initData: function(popupType, rec){
        var cr = this;
        var opts = this.opts;
        if (popupType == "Category") {
            const CatTemp = cr._baseAlanQweb("theme_alan.dialog_catGrid_list_view_init",rec);
            let $mainDataDiv = cr.$el.find(".as-cat-grid-select-list-view");
            $mainDataDiv.empty().append(CatTemp);
            $mainDataDiv.find(".as-sort-data").sortable();
        }
        let style_id = "#"+opts.styleUI;
        let dataCount = "#val"+opts.dataCount;
        cr.$el.find(style_id).prop("checked","checked");
        cr.$el.find(dataCount).prop("checked","checked");
        cr.$el.find(".dataPreview").addClass('d-none');
        var sPreview = ".s"+style_id.slice(-1);
        cr.$el.find(sPreview).removeClass('d-none');
        cr.$el.find(".imgPreview").addClass('d-none');
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

    _prodDataFetch(perent_id){
        let cr = this;
        let $selectedProduct = cr.$el.find(".as-cat-grid-select-list-view");
        let $perentDiv = $selectedProduct.find(".as-record-card-view[data-cat-id='"+perent_id+"']");
        if($perentDiv.attr("data-prod-data") == undefined || $perentDiv.attr("data-prod-ids") == undefined){
            return [{},[]];
        }
        let initDataDic = JSON.parse($perentDiv.attr("data-prod-data"));
        let initIds = JSON.parse($perentDiv.attr("data-prod-ids"));
        return [initDataDic,initIds];
    },

    _catDataFetch(){
        let cr = this;
        let $selectedCat = cr.$el.find(".as-cat-grid-select-list-view");
        let initDataDic = [];
        let initIds = [];
        let extraData = [];
        $selectedCat.find(".as-record-card-view").each(function (ind, ele) {
            initDataDic.push({'id': $(ele).data("catId"),'text': $(ele).data("catName") })
            initIds.push($(ele).data("catId"));
            extraData.push({'id': $(ele).data("catId"),
                'prodData': $(ele).data("prodData"),
                'prodIds': $(ele).data("prodIds")
            })
        });
        return [initDataDic,initIds,extraData];
    },

    _openProductDialog: function(ev) {
        let cr = this;
        let perent_id = $(ev.currentTarget).data("catId");
        let prePosData = cr._prodDataFetch(perent_id);
        let select2InitData = {
            fieldLabel: _t('Select Product'),
            coreTitle:_t('Product Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'CatProdGrid',
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
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'CatGrid',
            extraData:prePosData[2],
            parentDomain:false,
            customTemplate:'theme_alan.as_select2_category_dropdown'};
        cr.recordSelector = new recordSelector(cr,select2InitData);
        cr.recordSelector.open();
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
        let perentCat = cr._catDataFetch();
        var prodData = {};
        $.each(perentCat[1], function (ind, val) {
            let subCat = cr._prodDataFetch(val);
            prodData[val] = [subCat[0],subCat[1]];
        });
        let catIds = JSON.stringify(perentCat[1]);
        cr.src.$target.attr("data-cat-ids", catIds);
        cr.src.$target.attr('data-prod-ids', JSON.stringify(prodData));
        var dataCount = cr.$el.find("input[name='dataCount']:checked").val();
        let styleUI = cr.$el.find("input[name='layoutStyle']:checked").val();
        cr.src.$target.attr("data-dataCount", dataCount);
        cr.src.$target.attr("data-styleUI", styleUI);
        cr.$el.find(".as-close-dialog").trigger('click');
    },
});
return baseProduct
});