from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta, date
import calendar
from dateutil.relativedelta import relativedelta
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
import json
import io
from odoo.tools import date_utils
import base64
from collections import OrderedDict

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

DATE_DICT = {
    '%m/%d/%Y' : 'mm/dd/yyyy',
    '%Y/%m/%d' : 'yyyy/mm/dd',
    '%m/%d/%y' : 'mm/dd/yy',
    '%d/%m/%Y' : 'dd/mm/yyyy',
    '%d/%m/%y' : 'dd/mm/yy',
    '%d-%m-%Y' : 'dd-mm-yyyy',
    '%d-%m-%y' : 'dd-mm-yy',
    '%m-%d-%Y' : 'mm-dd-yyyy',
    '%m-%d-%y' : 'mm-dd-yy',
    '%Y-%m-%d' : 'yyyy-mm-dd',
    '%f/%e/%Y' : 'm/d/yyyy',
    '%f/%e/%y' : 'm/d/yy',
    '%e/%f/%Y' : 'd/m/yyyy',
    '%e/%f/%y' : 'd/m/yy',
    '%f-%e-%Y' : 'm-d-yyyy',
    '%f-%e-%y' : 'm-d-yy',
    '%e-%f-%Y' : 'd-m-yyyy',
    '%e-%f-%y' : 'd-m-yy'
}

FETCH_RANGE = 2000

class InsPartnerLedger(models.TransientModel):
    _inherit = "ins.partner.ledger"

    company_group_ids = fields.Many2many(
        "res.partner",
        "ins_partner_ledger_company_group_rel",
        "wizard_id", "partner_id",
        string="Company Groups",
        domain=[("is_company", "=", True)],
    )


    def action_pdf_company_group(self):
        data = self.read()[0]
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        sheet = workbook.add_worksheet('Partner Ledger')
        sheet.set_zoom(95)
        sheet_2 = workbook.add_worksheet('Filters')
        sheet_2.protect()

        record = self.env['ins.partner.ledger'].browse(data.get('id'))
        filters, account_lines = record.get_report_datas()

        sheet.set_column(0, 0, 18)  # VAT
        sheet.set_column(1, 1, 12)
        sheet.set_column(2, 2, 10)
        sheet.set_column(3, 3, 30)
        sheet.set_column(4, 4, 18)
        sheet.set_column(5, 5, 30)
        sheet.set_column(6, 6, 30)
        sheet.set_column(7, 9, 13)

        sheet.freeze_panes(4, 0)
        sheet.screen_gridlines = False
        sheet_2.screen_gridlines = False


        format_title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 12, 'font': 'Arial'})
        format_header = workbook.add_format({'bold': True, 'font_size': 10, 'align': 'center', 'font': 'Arial'})
        content_header = workbook.add_format({'font_size': 10, 'align': 'center', 'border': True, 'font': 'Arial'})
        content_header_date = workbook.add_format({'font_size': 10, 'align': 'center', 'border': True, 'font': 'Arial'})

        line_header = workbook.add_format(
            {'bold': True, 'font_size': 10, 'align': 'center', 'top': True, 'bottom': True, 'font': 'Arial'})
        line_header_light = workbook.add_format(
            {'font_size': 10, 'align': 'center', 'text_wrap': True, 'font': 'Arial', 'valign': 'top'})
        line_header_light_initial = workbook.add_format(
            {'italic': True, 'font_size': 10, 'align': 'center', 'bottom': True, 'font': 'Arial', 'valign': 'top'})
        line_header_light_initial_bold = workbook.add_format(
            {'bold': True, 'italic': True, 'font_size': 10, 'align': 'center', 'bottom': True, 'font': 'Arial',
             'valign': 'top'})
        line_header_light_ending = workbook.add_format(
            {'italic': True, 'font_size': 10, 'align': 'center', 'top': True, 'font': 'Arial', 'valign': 'top'})
        line_header_light_ending_bold = workbook.add_format(
            {'bold': True, 'italic': True, 'font_size': 10, 'align': 'center', 'bottom': True, 'font': 'Arial',
             'valign': 'top'})
        company_group_header = workbook.add_format(
            {'bold': True, 'font_size': 10, 'align': 'center', 'valign': 'vcenter', 'font': 'Arial',
             'bg_color': '#D9E1F2', 'border': 1})

        lang = self.env.user.lang
        lang_id = self.env['res.lang'].search([('code', '=', lang)], limit=1)
        currency_id = self.env.user.company_id.currency_id
        date_fmt = DATE_DICT.get(lang_id.date_format, 'dd/mm/yyyy')

        for fmt in (line_header, line_header_light, line_header_light_initial, line_header_light_ending):
            fmt.num_format = currency_id.excel_format

        line_header_light_date = workbook.add_format({'font_size': 10, 'align': 'center', 'font': 'Arial'})
        line_header_light_date.num_format = date_fmt
        content_header_date.num_format = date_fmt

        row_pos = 0
        group_names = ', '.join(self.company_group_ids.mapped('name')) if self.company_group_ids else \
        data['company_id'][1]
        sheet.merge_range(0, 0, 0, 9, _('Partner Ledger') + ' - ' + group_names, format_title)

        Partner = self.env['res.partner']
        grouped_lines = OrderedDict()

        for partner_id, vals in account_lines.items():
            partner = Partner.browse(partner_id)
            group_company = partner.company_group_id

            if self.company_group_ids and group_company not in self.company_group_ids:
                continue

            company = group_company or partner
            comp_entry = grouped_lines.setdefault(
                company.id,
                {'name': company.name, 'debit': 0.0, 'credit': 0.0, 'balance': 0.0, 'partners': []}
            )
            comp_entry['debit'] += vals['debit']
            comp_entry['credit'] += vals['credit']
            comp_entry['balance'] += vals['balance']
            comp_entry['partners'].append({
                'partner': partner,
                'name': vals['name'],
                'debit': vals['debit'],
                'credit': vals['credit'],
                'balance': vals['balance'],
            })

        # Header row
        row_pos += 3
        if filters.get('include_details', False):
            headers = [_('Tax ID'), _('Date'), _('JRNL'), _('Account'), _('Ref'), _('Move'), _('Entry Label'),
                       _('Debit'), _('Credit'), _('Balance')]
            for col, title in enumerate(headers):
                sheet.write(row_pos, col, title, format_header)
        else:
            sheet.write(row_pos, 0, _('Tax ID'), format_header)
            sheet.merge_range(row_pos, 1, row_pos, 6, _('Partner'), format_header)
            sheet.write(row_pos, 7, _('Debit'), format_header)
            sheet.write(row_pos, 8, _('Credit'), format_header)
            sheet.write(row_pos, 9, _('Balance'), format_header)

        for comp_data in grouped_lines.values():
            row_pos += 1
            sheet.merge_range(row_pos, 0, row_pos, 6, comp_data['name'], company_group_header)
            sheet.write(row_pos, 7, comp_data['debit'], company_group_header)
            sheet.write(row_pos, 8, comp_data['credit'], company_group_header)
            sheet.write(row_pos, 9, comp_data['balance'], company_group_header)

            for p_data in comp_data['partners']:
                row_pos += 1
                sheet.write(row_pos, 0, p_data['partner'].vat or '', line_header_light)
                sheet.merge_range(row_pos, 1, row_pos, 6, p_data['name'], line_header_light)
                sheet.write(row_pos, 7, p_data['debit'], line_header_light)
                sheet.write(row_pos, 8, p_data['credit'], line_header_light)
                sheet.write(row_pos, 9, p_data['balance'], line_header_light)

                if filters.get('include_details', False):
                    count, offset, sub_lines = record.build_detailed_move_lines(offset=0, partner=p_data['partner'].id,
                                                                                fetch_range=1000000)
                    for sub_line in sub_lines:
                        row_pos += 1
                        move_name = sub_line.get('move_name')
                        if move_name == 'Initial Balance':
                            sheet.write(row_pos, 6, move_name, line_header_light_initial_bold)
                            sheet.write(row_pos, 7, sub_line['debit'], line_header_light_initial)
                            sheet.write(row_pos, 8, sub_line['credit'], line_header_light_initial)
                            sheet.write(row_pos, 9, sub_line['balance'], line_header_light_initial)
                        elif move_name == 'Ending Balance':
                            sheet.write(row_pos, 6, move_name, line_header_light_ending_bold)
                            sheet.write(row_pos, 7, p_data['debit'], line_header_light_ending)
                            sheet.write(row_pos, 8, p_data['credit'], line_header_light_ending)
                            sheet.write(row_pos, 9, p_data['balance'], line_header_light_ending)
                        else:
                            date_str = fields.Date.from_string(sub_line['ldate']).strftime(lang_id.date_format)
                            sheet.write(row_pos, 0, p_data['partner'].vat or '', line_header_light)
                            sheet.write(row_pos, 1, date_str, line_header_light_date)
                            sheet.write(row_pos, 2, sub_line['lcode'], line_header_light)
                            sheet.write(row_pos, 3, sub_line['account_name'] or '', line_header_light)
                            sheet.write(row_pos, 4, sub_line['lref'] or '', line_header_light)
                            sheet.write(row_pos, 5, move_name, line_header_light)
                            sheet.write(row_pos, 6, sub_line['lname'] or '', line_header_light)
                            sheet.write(row_pos, 7, sub_line['debit'], line_header_light)
                            sheet.write(row_pos, 8, sub_line['credit'], line_header_light)
                            sheet.write(row_pos, 9, sub_line['balance'], line_header_light)

        workbook.close()
        output.seek(0)
        file_data = base64.b64encode(output.read())

        report_id = self.env['common.xlsx.out'].sudo().create({
            'filedata': file_data,
            'filename': 'PartnerLedger.xls'
        })

        output.close()

        return {
            'type': 'ir.actions.act_url',
            'url': (
                    '/web/binary/download_document?model=common.xlsx.out'
                    '&field=filedata&id=%s&filename=PartnerLedger.xls' % report_id.id
            ),
            'target': 'new',
        }

