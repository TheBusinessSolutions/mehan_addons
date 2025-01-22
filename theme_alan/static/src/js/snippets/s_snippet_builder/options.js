odoo.define('theme_alan.snippet_builder',function(require) {
'use strict';

var core = require('web.core');
var QWeb = core.qweb;
var options = require('web_editor.snippets.options');
var Dialog = require('web.Dialog');
var _t = core._t;

options.registry['js_alan_snippet_builder'] = options.Class.extend({
    xmlDependencies: ['/theme_alan/static/src/xml/snippets/alan_snippet_builder/alan_snippet_builder.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/homepage.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/sliders.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/banner.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/about.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/call_to_action.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/category.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/our_client.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/collection.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/contact_us.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/features.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/our_team.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/portfolio.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/price_table.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/promotion.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/services.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/shop_banner.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/testimonial.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/title_section.xml',
                      '/theme_alan/static/src/xml/snippets/alan_snippet_builder/templates/video_popup.xml' ],
    events:{ 'click':'_changeCollection' },
    _changeCollection:function(){
        this.select_snippet('click','true');
    },
    select_snippet: function(type, value) {
        var self = this;
        this.id = this.$target.attr('id');
        if(type == false || type == 'click'){
            var dialog = new Dialog(self, {
                size: 'extra-large',
                title: 'Alan Snippet Builder',
                $content: QWeb.render('theme_alan.builder_block'),
                buttons: [{text: _t('Save'), classes: 'btn-primary', close: true, click: function () {
                    var snippet = $("input[name='radio-snippet']:checked").closest('.snippet-as').find('textarea').val();
                    self.$target.empty().append(snippet);
                    var model = self.$target.parent().attr('data-oe-model');
                    if(model){
                        self.$target.parent().addClass('o_editable o_dirty');
                    }
                }}, {text: _t('Discard'), close: true}],
            });
            dialog.open();
            return self;
        }
    },
    onBuilt: function () {
        this._super();
        this.select_snippet('click', 'true');
    },
});

$(document).on('click', '.edit-snippet-builder-box .e-sb-tab label', function(){
    $('.edit-snippet-builder-box .e-sb-tab label').removeClass('e-sb-active');
    $(this).addClass('e-sb-active');
    var tagid = $(this).data('tag');
    $('.e-sb-tab--content').removeClass('active').addClass('d-none');
    $('#'+tagid).addClass('active').removeClass('d-none');
});

});