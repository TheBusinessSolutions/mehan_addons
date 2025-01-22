odoo.define('atharva_theme_base.as_img_hotspot', function (require) {
"use strict";

var core = require('web.core');
var options = require('web_editor.snippets.options');
const webUtils = require('web.utils');
const { BaseAlanQweb } = require("theme_alan.core_mixins");
const RecordSelectorDialog = require("theme_alan.recordSelector");
var weWidgets = require('wysiwyg.widgets');
var Common_dialog = require('theme_alan.common_modal');
var _t = core._t;
var popoverShow = false;
var QWeb = core.qweb;

options.SnippetOptionWidget.include({
    events: {
        'click .o_we_collapse_toggler': '_onCollapseTogglerClick',
        'click .add_img_hotspot':'_addHotSpotIcon',
    },
    _addHotSpotIcon:function(){
        var $block = '<div class="row hotspot"><p style="position: absolute;top:50%;left: 50%;transform: translate(-50%, -50%);" class="hs_icon cur" data-name="Block">\
        <a href="#" class="icon">icon</a>\
        </p></div>';
        this.$target.after($block);
        this.$target.parent().find('.cur').trigger('click').removeClass('cur');
    }
});

options.registry.img_hotspots_slider_actions = options.Class.extend(BaseAlanQweb,{
    xmlDependencies: ['/theme_alan/static/src/xml/snippets/hotspot_modal.xml'],
    events:{
        'click we-button.add_preview':'_showPreview',
        'change we-range.pos_left':'_setPositionLeft',
        'change we-range.pos_top':'_setPositionRight',
        'click we-select.hs_types':'_setHotspotType',
        'click we-button.modal_tpy':'_setRemovePS',
        'click we-button.st_pop_tpy':'_setstaticPopover',
        'click we-button.st_modal_tpy':'_setstaticModal',
        'click we-button.pop_tpy':'_setDynamicPopver',
        'click we-button.add_product':'_setProduct',
        'click .imagebox':'_setImage',
        'click .style_icon':'_setIcon'
    },
    popup_template_id: "Product_select_template",
    popup_title: _t("Select Product For Dynamic Popover"),
    _setstaticPopover:function(){
        this.$target.children().attr('data-toggle','popover').attr('data-html',true).attr('data-content','');
    },
    _setstaticModal:function(){
        this.$target.children().removeAttr('data-toggle data-html data-content');
    },
    _setIcon:function(evt){
        var getCls = $(evt.currentTarget).attr('data-select-data-attribute')
        this.$target.removeClass('st1 st2 st3').addClass(getCls)
    },
    _setImage:function(){
        var self = this;
        var dialog = new weWidgets.MediaDialog(this, {multiImages: false, onlyImages: true, mediaWidth: 1920});
        return new Promise(resolve => {
            dialog.on('save', this, function (attachments) {
                self.$target.attr('data-po_imgurl',$(attachments).attr('src'))
            });
            dialog.on('closed', this, () => resolve());
            dialog.open();
        });
    },
    _productData(){
        let cr = this;
        var prodId = cr.$target.attr('data-product-id');
        var prodName =  cr.$target.attr('data-product_name');
        var initDataDic = false
        var initIds = ""
        if(prodId != 0 && prodName != undefined){
            initDataDic = [{'id':Number(prodId.trim()),'text': prodName }] ;
            initIds = prodId.trim();
        }
        return [initDataDic,initIds];
    },
    _setProduct:function(){
        let cr = this;
        let prePosData = cr._productData();
        let select2InitData = {
            fieldLabel: _t('Select Product'),
            coreTitle:_t('Product Configuration'),
            route:"/get/select2/data",
            isMultiSelect:false,
            initData:prePosData[0][0],
            initIds:prePosData[1],
            searchType:'ImageHotspot',
            customTemplate:'theme_alan.as_select2_products_dropdown'};
        cr.recordSelector = new RecordSelectorDialog(cr,select2InitData);
        cr.recordSelector.open();
    },
    _setDynamicPopver:function(){
        var popoverhtm = "<div class='media'><h2>No Product Seleted</h2></div>";
        this.$target.children().attr('data-toggle','popover').attr('data-html',true).attr('data-content',popoverhtm);
    },
    _setRemovePS:function () {
        this.$target.removeAttr('data-po_style');
        this.$target.children().removeAttr('data-toggle data-html data-content');
    },
    _showPreview:function(){
        if(this.$target.attr("data-st_type") == "popover"){
            if(popoverShow === false){
                var title = this.$target.attr('data-po_title') == undefined ? '':this.$target.attr('data-po_title');
                var description = this.$target.attr('data-po_desc') == undefined ? '':this.$target.attr('data-po_desc');
                var btn_txt = this.$target.attr('data-po_btxt') == undefined ? '':this.$target.attr('data-po_btxt');
                var btn_url = this.$target.attr('data-po_bturl') == undefined ? '':this.$target.attr('data-po_bturl');
                var img_url = this.$target.attr('data-po_imgurl') == undefined ? '' :this.$target.attr('data-po_imgurl');
                var pop_thm = this.$target.attr('data-po_theme') == undefined ? '' :this.$target.attr('data-po_theme');
                var pop_style = this.$target.attr('data-po_style') == undefined ? '' :this.$target.attr('data-po_style');
                var style_cls = pop_thm + " " + pop_style;
                var popoverhtm = "<div class='hp-media "+ style_cls +"'>\<div class='hp-img'><img src='"+img_url+"' alt='Image'></div>\<div class='hp-media-body'>\<h5 class='hp-title'>"+ title +"</h5><p>"+description+"</p><a href='"+btn_url+"' class='as-btn as-btn-theme btn-sm'>"+ btn_txt +"</a></div></div>";
                this.$target.children().removeAttr('data-original-title').removeAttr('title');
                this.$target.children().attr('data-content',popoverhtm);
                var getData = this.$target.find('[data-toggle="popover"]').popover();
                this.$target.find('[data-toggle="popover"]').popover('show');
                var getid = "#" + $(getData['0']).attr('aria-describedby');
                $(getid).removeClass('dark_thm light_thm st1 st2 st3');
                style_cls =  'as-hotspot-popover' + '  '+ style_cls;
                $(getid).addClass(style_cls);
                popoverShow = true;
            }
            else{
                this.$target.find('[data-toggle="popover"]').popover('hide');
                popoverShow = false;
            }
        }
        else if(this.$target.attr("data-st_type") == "modal"){
            let cr = this;
            var title = this.$target.attr('data-po_title') == undefined ? '':this.$target.attr('data-po_title');
            var description = this.$target.attr('data-po_desc') == undefined ? '':this.$target.attr('data-po_desc');
            var btn_txt = this.$target.attr('data-po_btxt') == undefined ? '':this.$target.attr('data-po_btxt');
            var btn_url = this.$target.attr('data-po_bturl') == undefined ? '':this.$target.attr('data-po_bturl');
            var img_url = this.$target.attr('data-po_imgurl') == undefined ? '' :this.$target.attr('data-po_imgurl');
            var pop_thm = this.$target.attr('data-po_theme') == undefined ? '' :this.$target.attr('data-po_theme');
            var pop_style = this.$target.attr('data-po_style') == undefined ? '' :this.$target.attr('data-po_style');
            var style_cls = pop_thm + " " + pop_style;
            var context = {'title':title,'description':description,'btn_txt':btn_txt,'btn_url':btn_url,'img_url':img_url ,'theme':style_cls}

            var common_dialog = new Common_dialog(cr,{
                size: 'medium',
                subTemplate: webUtils.Markup($(this._baseAlanQweb("theme_alan.hotspot_static_modal", context)).html()),
            });
            common_dialog.open();
        }
    },
    _setPositionLeft:function(){
        var posval = this.$target.attr('data-pos_left');
        posval = posval+"%";
        this.$target.css('left',posval);
    },
    _setPositionRight:function(){
        var posval = this.$target.attr('data-pos_top');
        posval = posval+"%";
        this.$target.css('top',posval);
    },
    _setHotspotType:function(){
        this.$target.children().removeAttr('data-toggle data-html data-content');
        if(this.$target.hasClass('dynamic_type')){
            this.$target.removeAttr('data-po_title data-po_desc data-po_btxt data-po_imgurl data-po_bturl data-po_style data-po_theme').attr('data-product-id','0')
        }
    },
    cleanForSave:function(){
        if(popoverShow == true){
            this._showPreview();
        }
        var title = this.$target.attr('data-po_title') == undefined ? '':this.$target.attr('data-po_title');
        var description = this.$target.attr('data-po_desc') == undefined ? '':this.$target.attr('data-po_desc');
        var btn_txt = this.$target.attr('data-po_btxt') == undefined ? '':this.$target.attr('data-po_btxt');
        var btn_url = this.$target.attr('data-po_bturl') == undefined ? '':this.$target.attr('data-po_bturl');
        var img_url = this.$target.attr('data-po_imgurl') == undefined ? '' :this.$target.attr('data-po_imgurl');
        var pop_thm = this.$target.attr('data-po_theme') == undefined ? '' :this.$target.attr('data-po_theme');
        var pop_style = this.$target.attr('data-po_style') == undefined ? '' :this.$target.attr('data-po_style');
        $(".hs_icon").each(function (index, element) {
            if($(this).hasClass("static_type") === false && $(this).hasClass("dynamic_type") == false){
                $(this).parent().remove();;
            }
        });
    }
});
});
