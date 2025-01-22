# -*-coding: utf-8 -*-
from odoo import api, fields, models


class OrderReport(models.AbstractModel):
    _name = 'report.n2d_so_categ_inlines.order_report_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        quant_obj = self.env["stock.quant"]
        products = self.env['product.product']

        start = data['start']
        end = data['end']
        date_start = data['date_start']
        date_end = data['date_end']
        location_id = data['location_id']
        product_id = data['product_id']

        if product_id :
            quants = quant_obj.search([('product_id', '=', product_id),('location_id', 'child_of', location_id)])
        else:
            quants = quant_obj.search([('location_id', 'child_of', location_id)])

        products |= quants.mapped('product_id')

        if product_id :
            moves = self.env['stock.move'].search([
                ('date', '>=', start),
                ('date', '<=', end),
                ('state', '=', 'done'),
                ('product_id', '=', product_id),
                '|',
                ('location_dest_id', 'child_of', location_id),
                ('location_id', 'child_of', location_id)])
            moves_to_now = self.env['stock.move'].search([
                ('date', '>=', end),
                ('date', '<=', fields.Datetime.now()),
                ('state', '=', 'done'),
                ('product_id', '=', product_id),
                '|',
                ('location_dest_id', 'child_of', location_id),
                ('location_id', 'child_of', location_id)])
        else :
            moves = self.env['stock.move'].search([
                ('date', '>=', start),
                ('date', '<=', end),
                ('state', '=', 'done'),
                '|',
                ('location_dest_id', 'child_of', location_id),
                ('location_id', 'child_of', location_id)])
            moves_to_now = self.env['stock.move'].search([
                ('date', '>=', end),
                ('date', '<=', fields.Datetime.now()),
                ('state', '=', 'done'),
                '|',
                ('location_dest_id', 'child_of', location_id),
                ('location_id', 'child_of', location_id)])

        location = self.env['stock.location'].browse(location_id)
        location_ids = self.env['stock.location'].search([
            ('parent_left', '>=', location.parent_left),
            ('parent_right', '<=', location.parent_right)])

        mv_in = moves.filtered(
            lambda x: x.location_dest_id.id in location_ids.ids)
        mv_out = moves.filtered(
            lambda x: x.location_id.id in location_ids.ids)
        mv_tonow_in = moves_to_now.filtered(
            lambda x: x.location_dest_id.id in location_ids.ids)
        mv_tonow_out = moves_to_now.filtered(
            lambda x: x.location_id.id in location_ids.ids)

        products |= mv_in.mapped("product_id")
        products |= mv_out.mapped("product_id")

        datas = {}
        datas['warehouse'] = data['warehouse_name']
        datas['location'] = data['location_name']
        datas['date_from'] = fields.Datetime.from_string(date_start).strftime("%Y-%m-%d")
        datas['date_to'] = fields.Datetime.from_string(date_end).strftime("%Y-%m-%d")
        datas['product_id'] = product_id or False

        result = []
        for product in products:
            line = {}
            line['name'] = product.name
            line['price'] = product.list_price
            line['ref'] = product.default_code
            line['uom'] = product.uom_id.name

            mv_in_pro = mv_in.filtered(
                lambda x: x.product_id.id == product.id)
            mv_out_pro = mv_out.filtered(
                lambda x: x.product_id.id == product.id)
            mv_tonow_in_pro = mv_tonow_in.filtered(
                lambda x: x.product_id.id == product.id)
            mv_tonow_out_pro = mv_tonow_out.filtered(
                lambda x: x.product_id.id == product.id)

            product_uom = product.uom_id
            tot_in = 0
            for elt in mv_in_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_in += elt.product_uom_qty * factor

            tot_out = 0
            for elt in mv_out_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_out += elt.product_uom_qty * factor

            tot_tonow_in = 0
            for elt in mv_tonow_in_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_tonow_in += elt.product_uom_qty * factor

            tot_tonow_out = 0
            for elt in mv_tonow_out_pro:
                if product_uom.id != elt.product_uom.id:
                    factor = product_uom.factor / elt.product_uom.factor
                else:
                    factor = 1.0
                tot_tonow_out += elt.product_uom_qty * factor

            actual_qty = product.with_context(
                {'location': location_id}).qty_available
            actual_qty += tot_tonow_out - tot_tonow_in

            line['si'] = actual_qty - tot_in + tot_out
            line['in'] = tot_in
            line['out'] = tot_out
            line['bal'] = tot_in - tot_out
            line['fi'] = actual_qty
            line['Bala*price'] = line['fi'] * line['price']

            result.append(line)

        datas['lines'] = result

        return {'doc_ids': docids, 'data': datas}
