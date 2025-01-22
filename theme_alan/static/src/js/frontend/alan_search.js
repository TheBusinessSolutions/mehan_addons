// /** @odoo-module alias=theme_alan.advance_search **/

import websiteSearch from '@website/snippets/s_searchbar/000';
import {qweb} from 'web.core';
import {Markup} from 'web.utils';

var { searchBar } = websiteSearch;

searchBar.include({
    xmlDependencies:['/theme_alan/static/src/xml/alan_search_bar.xml', '/website/static/src/snippets/s_searchbar/000.xml'],
    _render: function (res) {
        const $prevMenu = this.$menu;
        this.$el.toggleClass('dropdown show', !!res);
        if (res && this.limit) {
            const results = res['results'];
            if (this.searchType == 'as_advance_search') {
                var template = 'theme_alan.s_alan_searchbar.autocomplete';
            }else{
                var template = 'website.s_searchbar.autocomplete';
            }
            const candidate = template + '.' + this.searchType;
            if (qweb.has_template(candidate)) {
                template = candidate;
            }
            this.$menu = $(qweb.render(template, {
                results: results,
                brands: res['brands'],
                tags: res['tags'],
                category: res['category'],
                products: res['products'],
                parts: res['parts'],
                hasMoreResults: results.length < res['results_count'],
                search: this.$input.val(),
                fuzzySearch: res['fuzzy_search'],
                widget: this,
            }));
            this.$menu.css('min-width', this.autocompleteMinWidth);
            this.$el.append(this.$menu);
            this.$el.find('button.extra_link').on('click', function (event) {
                event.preventDefault();
                window.location.href = event.currentTarget.dataset['target'];
            });
            this.$el.find('.s_searchbar_fuzzy_submit').on('click', (event) => {
                event.preventDefault();
                this.$input.val(res['fuzzy_search']);
                const form = this.$('.o_search_order_by').parents('form');
                form.submit();
            });
        }
        if ($prevMenu) {
            $prevMenu.remove();
        }
    },
    async _fetch() {
        if(this.searchType == "as_advance_search"){
            const res = await this._rpc({
                route: '/website/snippet/autocomplete',
                params: {
                    'search_type': this.searchType,
                    'term': this.$input.val(),
                    'order': this.order,
                    'limit': this.limit,
                    'max_nb_chars': Math.round(Math.max(this.autocompleteMinWidth, parseInt(this.$el.width())) * 0.22),
                    'options': this.options,
                },
            });
            const fieldNames = [
                'name',
                'description',
                'extra_link',
                'detail',
                'detail_strike',
                'detail_extra',
            ];
            if(res.products == undefined){
                res.products = [];
            }
            if(res.brands == undefined){
                res.brands = [];
            }
            if(res.tags == undefined){
                res.tags = [];
            }
            if(res.category == undefined){
                res.category = [];
            }
            const as_srch_lst = [res.products, res.brands, res.tags, res.category];
            as_srch_lst.forEach(ele => {
                ele.forEach(record => {
                    for (const fieldName of fieldNames) {
                        if (record[fieldName]) {
                            if (typeof record[fieldName] === "object") {
                                for (const fieldKey of Object.keys(record[fieldName])) {
                                    record[fieldName][fieldKey] = Markup(record[fieldName][fieldKey]);
                                }
                            } else {
                                record[fieldName] = Markup(record[fieldName]);
                            }
                        }
                    }
                });
            });
            return res;
        }
        else{
            return this._super.apply(this, arguments);
        }

    },
})
export default {
    searchBar: searchBar,

}