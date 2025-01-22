# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odoo Website Product Variant Description',
    'summary':'Show Product Variant Description on Website item Variant Description for website Product Description shop product variants details shop Product Variant details shop Product Variants website product attributes category website product Variants Description',
    'description': """

    This module is used to website manage different product Variant description on webshop product Variant description on website
    product Variant description on eCommerce inculding following feature.
    Website product Variant Description Webshop product Variant Description Website Variant Description 
    Show different Variant Description on website Show Different product variant description on webshop 
    Show Different product variant description on Website product description on website 

    webshop manage different webshop product Variant description on website product Variant description on webstore
    webstore product Variant description on eCommerce inculding following feature.
    webshop product Variant Description webstore product Variant Description eCommerce Variant Description 
    eCommerce how different Variant Description on eCommerce Show Different product variant description on eCommerce 
    eCommerce Show Different product variant description on webshop product description on webstore 

    eCommerce manage different eCommerce product Variant description on eCommerce product Variant description on webstore
    e-Commerce product Variant description on e-Commerce inculding following feature.
    webstote product Variant Description e Commerce product Variant Description e Commerce Variant Description 
    e-Commerce how different Variant Description on e Commerce Show Different product variant description on eCommerce 
    e-Commerce Show Different product variant description on website product description of Variant on e-Commerce 
This Odoo apps helps you to display variant wise description on odoo Website and Odoo webshop for each product variant. Default Odoo shows product description on webstore from the product template so if you have multiple variants for same product i.e colour, size, brand, memory etc then those all product variant display same description for all, But using this odoo module apps
we will allow user to add different description for each product variant and when visitors of website or webshop user select different variants of product description of that selected variants displayed on odoo webshop.

""" ,
    "price": 49,
    "currency": 'EUR',
    'category': 'eCommerce',
    'version': '15.0.0.0',
    'author': 'BrowseInfo',
    'website':'https://www.browseinfo.in',
    'depends': ['website','website_sale'],
    'data': [
        'views/template.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'OPL-1',
    'live_test_url':'https://youtu.be/YL4IYrMpPEQ',
    "images":['static/description/Banner.png'],
    'assets': {
        'web.assets_frontend': [
            'website_product_variant_description/static/src/css/custom.css',
            'website_product_variant_description/static/src/js/custom.js',
        ],
    }
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
