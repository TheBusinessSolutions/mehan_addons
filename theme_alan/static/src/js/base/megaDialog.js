odoo.define('theme_alan.core_mega_dialog', function (require) {
"use strict";

const webEditor = require('web_editor.widget');
const webCore = require('web.core');
const webUtils = require('web.utils');
const megaDialog = webEditor.Dialog;
const _t = webCore._t;
const RecordSelectorDialog = require("theme_alan.recordSelector");
const { AlanTemplateGetter,
        FetchProductsData,
        FetchCategoryData,
        BaseAlanQweb } = require("theme_alan.core_mixins");

let BaseMega = megaDialog.extend(AlanTemplateGetter, FetchProductsData, FetchCategoryData, BaseAlanQweb,{
    template: 'theme_alan.core_dialog',
    xmlDependencies: megaDialog.prototype.xmlDependencies.concat([
        '/theme_alan/static/src/xml/core_dialog.xml',
        '/theme_alan/static/src/xml/record_list_view.xml',]),
    events: _.extend({}, megaDialog.prototype.events, {
        'click .as-save-dialog': '_onSavebtn',
        'click .as-close-dialog': 'close',
        'click #mega-add-btn-prod':'_openProductSelectorDialog',
        'click #mega-add-btn-cat':'_openCategorySelectorDialog',
        'click .as-add-sub-cat-btn':'_openSubCategorySelectorDialog',
        'click .as-record-rm-btn':'_removeRecordDiv',
        'change input[name="megaView"]':'_changeMegaStyle',
    }),
    willStart:function(){
        var cr = this;
        return cr._super.apply(cr, arguments).then(function(){
            if(cr.opts.megaPopup == "theme_alan.product_mega_modal" || cr.opts.megaPopup == "product_mega_modal"){
                if(cr.opts.initRecords != undefined && cr.opts.megaUi != undefined){
                    cr._fetchProductRawData(cr.opts.initRecords,"product.template").then(function(rec){
                        if(typeof(cr.opts.initRecords) == "string"){
                            if(cr.opts.initRecords.trim() != ""){
                                cr._initData(rec,"Product");
                            }
                        }else{
                            cr._initData(rec,"Product");
                        }
                    });
                }
            }
            else if(cr.opts.megaPopup == "theme_alan.category_mega_modal" || cr.opts.megaPopup == "category_mega_modal"){
                if(cr.opts.initRecords != undefined && cr.opts.megaUi != undefined){
                    if(cr.opts.initRecords.trim() != ""){
                        var initData = JSON.parse(cr.opts.initRecords.replace(/'/g,'"'));
                        cr._fetchCategoryRawData(cr.opts.catSeq).then(function(rec){
                            var clean_res = [];
                            _.each(rec, function (res) {
                                let subcatData = initData[res['id']];
                                res['subCatData'] =  JSON.stringify(subcatData[0]);
                                res['subCatIds'] = JSON.stringify(subcatData[1]);
                                clean_res.push(res);
                            });
                            cr._initData(clean_res,"Category");
                        });
                    }
                }
            }
        });
    },
    init: function (src, opts) {
        var cr = this;
        cr._super(src, _.extend({ fullSubTemplate: opts.fullSubTemplate || 0,
            enableCoreButton: opts.enableCoreButton,enableCoreTitle: opts.enableCoreTitle,
            subTemplate: opts.subTemplate || "",initRecords: opts.initRecords || "",
            catSeq:opts.catSeq || "",megaUi: opts.megaUi || "",
            colUi: opts.colUi || "",megaPopup:opts.megaPopup || "",
            coreTitle: opts.coreTitle || _t('Configuration'),
            size: opts.size || 'extra-large', dialogClass:'as-edit-core-modal',
            renderHeader: 0, renderFooter: 0 }));
        cr.src = src;
        cr.opts = opts;
    },
    _initData:function (rec, megaType) {
        var cr = this;
        if(megaType == "Product"){
            var opts = this.opts;
            let clean_res = []
            for (const r of rec) {
                r['price'] = webUtils.Markup(r['price']);
                clean_res.push(r);
            }
            const ProdTemp = cr._baseAlanQweb("theme_alan.dialog_product_list_view",clean_res);
            let $mainDataDiv = cr.$el.find(".as-product-select-list-view");
            $mainDataDiv.empty().append(ProdTemp);
            $mainDataDiv.find(".as-sort-data").sortable();
            let ui_id = "#"+opts.megaUi;
            let col_id = "#"+opts.colUi;
            cr.$el.find(ui_id).prop("checked","checked");
            cr.$el.find(col_id).prop("checked","checked");
            let $megaPre = cr.$el.find(".megaPreview").addClass("d-none");
            $($megaPre).each(function (ind, ele) {
                if($(ele).attr("data-style-id") == opts.megaUi){
                    $(ele).removeClass("d-none");
                }
            });
        }
        else if(megaType == "Category"){
            var opts = cr.opts;
            const ProdTemp =  cr._baseAlanQweb("theme_alan.dialog_cat_list_view",rec);
            let $mainDataDiv = cr.$el.find(".as-category-select-list-view");
            $mainDataDiv.empty().append(ProdTemp);
            $mainDataDiv.find(".as-sort-data").sortable();
            let ui_id = "#"+opts.megaUi;
            let col_id = "#"+opts.colUi;
            cr.$el.find(ui_id).prop("checked","checked");
            cr.$el.find(col_id).prop("checked","checked");
            let $megaPre = cr.$el.find(".megaPreview").addClass("d-none");
            $($megaPre).each(function (ind, ele) {
                if($(ele).attr("data-style-id") == opts.megaUi){ $(ele).removeClass("d-none") }
            });
        }
    },
    _productMegaMenuDataFetch(){
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
    _categoryMegaMenuDataFetch(){
        let cr = this;
        let $selectedProduct = cr.$el.find(".as-category-select-list-view");
        let initDataDic = [];
        let initIds = [];
        let extraData = [];
        $selectedProduct.find(".as-record-card-view").each(function (ind, ele) {
            initDataDic.push({'id': $(ele).data("catId"),'text': $(ele).data("catName") })
            initIds.push($(ele).data("catId"));
            extraData.push({'id': $(ele).data("catId"),
            'subCatData': $(ele).data("subCatData"),
            'subCatIds': $(ele).data("subCatIds")
            })
        });
        return [initDataDic,initIds,extraData];
    },
    _subCategoryMegaMenuDataFetch:function(perent_id){
        let cr = this;
        let $selectedProduct = cr.$el.find(".as-category-select-list-view");
        let $perentDiv = $selectedProduct.find(".as-record-card-view[data-cat-id='"+perent_id+"']");
        if($perentDiv.attr("data-sub-cat-data") == undefined || $perentDiv.attr("data-sub-cat-ids") == undefined){
            return [{},[]];
        }
        let initDataDic = JSON.parse($perentDiv.attr("data-sub-cat-data"));
        let initIds = JSON.parse($perentDiv.attr("data-sub-cat-ids"));
        return [initDataDic,initIds];
    },
    _openProductSelectorDialog: function(ev){
        let cr = this;
        let prePosData = cr._productMegaMenuDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Product'),
            coreTitle:_t('Product Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            searchType:'Product',
            customTemplate:'theme_alan.as_select2_products_dropdown'};
        cr.recordSelector = new RecordSelectorDialog(cr,select2InitData);
        cr.recordSelector.open();
    },
    _openCategorySelectorDialog:function(){
        let cr = this;
        let prePosData = cr._categoryMegaMenuDataFetch();
        let select2InitData = {
            fieldLabel: _t('Select Category'),
            coreTitle:_t('Category Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            extraData:prePosData[2],
            parentDomain:false,
            searchType:'Category',
            customTemplate:'theme_alan.as_select2_category_dropdown' };
        cr.recordSelector = new RecordSelectorDialog(cr, select2InitData);
        cr.recordSelector.open();
    },
    _openSubCategorySelectorDialog:function(ev){
        let cr = this;
        let perent_id = $(ev.currentTarget).data("catId");
        let prePosData = cr._subCategoryMegaMenuDataFetch(perent_id);
        let select2InitData = {
            fieldLabel: _t('Select Sub Category'),
            coreTitle:_t('Sub Category Configuration'),
            route:"/get/select2/data",
            isMultiSelect:true,
            initData:prePosData[0],
            initIds:prePosData[1].join(","),
            parentDomain:perent_id,
            searchType:'SubCategoryLevel1',
            customTemplate:'theme_alan.as_select2_category_dropdown' };
        cr.recordSelector = new RecordSelectorDialog(cr, select2InitData);
        cr.recordSelector.open();
    },
    _changeMegaStyle:function(ev){
        let cr = this;
        let preVal = $(ev.currentTarget).val();
        let $megaPre = cr.$el.find(".megaPreview").addClass("d-none");
        $($megaPre).each(function (ind, ele) {
            if($(ele).attr("data-style-id") == preVal){
                $(ele).removeClass("d-none");
            }
        });
    },
    start: function () {
        let cr = this;
        if(cr.opts.fullSubTemplate){ cr.$modal.find('.modal-content').addClass('as-full-modal'); }
        cr.$modal.find('.modal-dialog').addClass('modal-dialog-centered');
        return cr._super.apply(cr, arguments);
    },
    _removeRecordDiv:function(ev){
        $(ev.currentTarget).parents(".as-record-card-view").remove();
    },
    _onSavebtn: function (ev) {
        var cr = this;
        if(cr.opts.megaPopup == "theme_alan.product_mega_modal" || cr.opts.megaPopup == "product_mega_modal"){
            let prePosData = cr._productMegaMenuDataFetch();
            let prodIds = JSON.stringify(prePosData[1]);
            let megaUI = cr.$el.find("input[name='megaView']:checked").val();
            let colUI = cr.$el.find("input[name='columnView']:checked").val();
            cr.src.$target.attr("data-record-ids",prodIds);
            cr.src.$target.attr("data-mega-ui",megaUI);
            cr.src.$target.attr("data-col-ui",colUI);
            cr._fetchProductRawData(prePosData[1],"product.template").then((rec) =>{
                if(rec != undefined){
                    let clean_res = []
                    rec.forEach(ele => {
                        ele['price'] = webUtils.Markup(ele['price'])
                        clean_res.push(ele);
                    })
                    let data = { "mega_ui":megaUI, "prod_ids":prodIds, "col_ui":colUI,
                        "mega_data":clean_res, 'is_dynamic':true }
                    let megaProdView = cr.src.$target.attr("data-prod-mega-view");
                    if(megaProdView == "list"){
                        cr._getAlanTemplate("atharva_theme_base","as_mm_product_list",data).then((res) =>{
                            cr.src.$target.parent().empty().append(res['template']);
                        });
                    }else if(megaProdView == "grid"){
                        cr._getAlanTemplate("atharva_theme_base","as_mm_product_grid",data).then((res) =>{
                            cr.src.$target.parent().empty().append(res['template']);
                        });
                    }else{
                        alert("Something went wrong!")
                    }
                }else{
                    cr.src.$target.empty();
                    cr.close();
                }
            });
        }
        else if(cr.opts.megaPopup == "theme_alan.category_mega_modal" || cr.opts.megaPopup == "category_mega_modal"){
            let perentCat = cr._categoryMegaMenuDataFetch();
            var catData = {};
            $.each(perentCat[1], function (ind, val) {
                let subCat = cr._subCategoryMegaMenuDataFetch(val);
                catData[val] = [subCat[0],subCat[1]];
            });
            let megaUI = cr.$el.find("input[name='megaView']:checked").val();
            let colUI = cr.$el.find("input[name='columnView']:checked").val();
            let view = cr.src.$target.attr("data-cat-mega-view");
            cr.src.$target.attr('data-record-ids', JSON.stringify(catData));
            cr.src.$target.attr("data-mega-ui",megaUI);
            cr.src.$target.attr("data-col-ui",colUI);
            cr._fetchMegaCategoryTemplate(view,catData,megaUI,colUI,perentCat[1]).then((rec) => {
                cr.src.$target.parent().empty().append(rec['template']);
            });
        }
    },
});
return BaseMega;
});