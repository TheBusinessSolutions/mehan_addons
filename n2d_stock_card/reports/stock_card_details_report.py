# -*-coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import Warning
from datetime import datetime
import logging
import pytz

FORMAT_DATE = "%Y-%m-%d %H:%M:%S"
ERREUR_FUSEAU = _("Set your timezone in preferences")


def convert_UTC_TZ(self, UTC_datetime):
    if not self.env.user.tz:
        raise Warning(ERREUR_FUSEAU)
    local_tz = pytz.timezone(self.env.user.tz)
    date = datetime.strptime(
        str(UTC_datetime.replace(microsecond=0)), FORMAT_DATE)
    date = pytz.utc.localize(date, is_dst=None).astimezone(local_tz)
    # return date.strftime(FORMAT_DATE)
    return date.strftime('%Y-%m-%d')


def format_num(self, value):
    return f"{value:,.3f}"


_logger = logging.getLogger(__name__)


class StockCardDetailsReport(models.AbstractModel):
    _name = 'report.n2d_stock_card.stock_card_details_template'

    @api.model
    def _get_report_values(self, docids, data=None):

        quant_obj = self.env["stock.quant"]
        products = self.env['product.product']

        start = data['start']
        end = data['end']
        date_start = data['date_start']
        date_end = data['date_end']
        location_id = data['location_id']
        product_ids = data['product_ids'] or False

        if product_ids:
            quants = quant_obj.search(
                [('product_id', 'in', product_ids), ('location_id', 'child_of', location_id)])
        else:
            quants = quant_obj.search(
                [('location_id', 'child_of', location_id)])

        products |= quants.mapped('product_id')

        if product_ids:
            moves = self.env['stock.move'].search([
                ('date', '>=', start),
                ('date', '<=', end),
                ('state', '=', 'done'),
                ('product_id', 'in', product_ids),
                '|',
                ('location_dest_id', 'child_of', location_id),
                ('location_id', 'child_of', location_id)])
            moves_to_now = self.env['stock.move'].search([
                ('date', '>=', end),
                ('date', '<=', fields.Datetime.now()),
                ('state', '=', 'done'),
                ('product_id', 'in', product_ids),
                '|',
                ('location_dest_id', 'child_of', location_id),
                ('location_id', 'child_of', location_id)])
        else:
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
        location_ids = self.env['stock.location'].search(
            [('id', 'child_of', location.id)])

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
        datas['date_from'] = date_start
        datas['date_to'] = date_end

        datas['product_ids'] = product_ids or False

        result = []
        tot_tot_amount = 0.0
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

            # This line get the last stock valuation layer record before the selected start date.
            product_value_layer = self.env['stock.valuation.layer'].search(
                [('product_id', '=', product.id),
                 ('create_date', '<', start)], order='create_date desc', limit=1)

            # This line get the last unit cost of the product in valuation layer if exists and
            # if not exists get the standard price
            si_unit_cost = product_value_layer.unit_cost or product.standard_price
            si = actual_qty - tot_in + tot_out
            # Calculate the init stock value amount
            si_tot_amount = si_unit_cost * si

            line['si'] = format_num(self, si)
            line['si_unit_cost'] = format_num(self, si_unit_cost)
            line['si_tot_amount'] = format_num(self, si_tot_amount)

            line['in'] = format_num(self, tot_in)
            line['out'] = format_num(self, tot_out)
            line['bal'] = format_num(self, tot_in - tot_out)
            line['fi'] = format_num(self, actual_qty)
            line['tot_amount'] = si_tot_amount
            line['tot_amount_orig'] = si_tot_amount
            result.append(line)

            move_in_show = mv_in_pro - mv_tonow_in_pro
            move_out_show = mv_out_pro - mv_tonow_out_pro

            move_to_show = self.env['stock.move']
            move_to_show |= move_in_show
            move_to_show |= move_out_show
            move_to_show.sorted(lambda r: r.date)
            line['lines'] = []
            val_in = actual_qty - tot_in + tot_out
            val_fin = val_in
            tot_amount = si_tot_amount
            for mv in move_to_show:

                src = mv.location_id.id
                dst = mv.location_dest_id.id
                qty = mv.product_uom_qty

                val_in = qty if dst in location_ids.ids else 0
                val_out = qty if src in location_ids.ids else 0
                val_bal = val_in - val_out
                val_fin += val_bal

                mvdate = convert_UTC_TZ(self, mv.date) if mv.date else ""

                # This line get the last stock valuation layer record for a specific stock movement.
                value_layer = self.env['stock.valuation.layer'].search(
                    [('stock_move_id', '=', mv.id)], order='create_date desc', limit=1)

                # Unit cost for the movement or the standard price of the product
                unit_cost = value_layer.unit_cost or mv.product_id.standard_price

                val_in_out = val_in if val_in > 0 else (
                    val_out * -1) if val_out > 0 else 0

                val_amount = unit_cost * val_in_out
                # This line calculate total value amount base on the avarage unit cost
                # tot_amount = tot_amount + val_amount

                # This line calculate total value amount base on the last unit cost
                tot_amount = unit_cost * actual_qty

                elt = {}
                elt['mv'] = mv.reference or "-"
                elt['date'] = str(mvdate) or "-"
                elt['in'] = format_num(self, val_in)
                elt['out'] = format_num(self, val_out)
                elt['bal'] = format_num(self, val_bal)
                elt['fi'] = format_num(self, val_fin)

                elt['unit_cost'] = format_num(self, unit_cost)
                elt['val_mount'] = format_num(self, val_amount)

                line['tot_amount'] = format_num(self, tot_amount)
                line['tot_amount_orig'] = tot_amount

                line['lines'].append(elt)

        # Calculating total of all value amount for all products to get the total value amount in a specific stock location
        for ln in result:
            tot_tot_amount = tot_tot_amount + ln["tot_amount_orig"]

        datas['lines'] = result
        datas['tot_tot_amount'] = format_num(self, tot_tot_amount)

        return {'doc_ids': docids, 'data': datas}
