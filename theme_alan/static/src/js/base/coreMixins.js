odoo.define('theme_alan.core_mixins', function (require) {
"use strict";

var ajax = require('web.ajax');
const webUtils = require('web.utils');
const webCore = require('web.core');

// var coreData =  {
var AlanTemplateGetter = {
        _getAlanTemplate:function(module, t_name, data){
            const template = module + "." + t_name;
            return this._rpc({
                route: '/alan_template_getter',
                params: { 'template':template, 'data':data}
            });
        },
    }

var FetchProductsData = {
        _fetchProductRawData:function(prod_vals, model){
            return this._rpc({
                route: '/get/product/raw/data',
                params: { 'product_ids':prod_vals, 'model':model }
            });
        },
    }
var FetchCategoryData = {
        _fetchCategoryRawData:function(cat_vals){
            return this._rpc({
                route: '/get/category/raw/data',
                params: { 'category_ids':cat_vals }
            });
        },
        _fetchMegaCategoryTemplate:function(view, cat_data=false, cat_ui=false, col_ui=false, cat_ids=false, do_json=false){
            return this._rpc({
                route: '/get/category/mega/template',
                params: {
                    'view':view,
                    'category_data':cat_data,
                    'category_ids':cat_ids,
                    'category_ui':cat_ui,
                    'column_ui':col_ui,
                    'do_json':do_json
                }
            });
        },
    }
var FetchBrandData = {
        _fetchBrandRawData:function(brand_vals){
            return this._rpc({
                route: '/get/brand/raw/data',
                params: {'brand_ids': brand_vals}
            });
        },
    }
var FetchBlogData = {
        _fetchBlogRawData:function(blog_vals){
            return this._rpc({
                route: '/get/blog/raw/data',
                params: {'blog_ids': blog_vals}
            });
        },
    }
var AjaxAddToCart = {
        _alanAddToCart:function(params){
            return ajax.jsonRpc('/shop/cart/update_json', 'call', {
                product_id: Number(params.product_id),
                line_id:params.line_id || undefined,
                add_qty:params.add_qty || undefined,
                set_qty:params.set_qty || undefined,
                no_variant_attribute_values:params.no_variant_attribute_values || "[]",
                product_custom_attribute_values:params.product_custom_attribute_values || "[]",
            })
        },
        _alanMiniCart:function(){
            return ajax.jsonRpc('/shop/mini/cart', 'call', {})
        }
    }
var BaseAlanQweb = {
        _baseAlanQweb: function(template,context){
            return webCore.qweb.render(template, {
                data: context
            });
        }
}

function alanUpdateCartNavBar(data) {
    var $qtyNavBar = $(".my_cart_quantity");
    _.each($qtyNavBar, function (qty) {
        var $qty = $(qty);
        $qty.parents('li:first').removeClass('d-none');
        $qty.addClass('o_mycart_zoom_animation').delay(300).queue(function () {
            $(this).text(data.cart_quantity);
            $(this).removeClass("o_mycart_zoom_animation").dequeue();
        });
    });
    $(".js_cart_lines").first().before(data['website_sale.cart_lines']).end().remove();
    $(".js_cart_summary").first().before(data['website_sale.short_cart_summary']).end().remove();
    var $head_cart_amt = $(".as_header_cart_amt");
    if($head_cart_amt.length > 0){
        $(".as_header_cart_amt").first().empty().append(webUtils.Markup(
            $(data["website_sale.short_cart_summary"])
            .find("#order_total_untaxed")
            .find(".monetary_field").html()));
    }
}

return {
    AlanTemplateGetter:AlanTemplateGetter,
    FetchProductsData:FetchProductsData,
    FetchCategoryData:FetchCategoryData,
    FetchBrandData:FetchBrandData,
    FetchBlogData:FetchBlogData,
    AjaxAddToCart:AjaxAddToCart,
    BaseAlanQweb:BaseAlanQweb,
    alanUpdateCartNavBar:alanUpdateCartNavBar
}
});
