# -*- coding: utf-8 -*-

from tracemalloc import DomainFilter
from odoo import fields, models
from odoo.exceptions import ValidationError


class VatReport(models.TransientModel):
    _name = "vat.report"

    date_from = fields.Date(string='Date from', default=fields.Date.context_today, required=True)
    date_to = fields.Date(string='Date to', default=fields.Date.context_today, required=True)
    account_type = fields.Selection(
        selection=[('customer_invoices', 'Customer Invoices'), ('supplier_invoices', 'Supplier Invoices'),
                   ('both', 'Both')], string='Account Type', default='customer_invoices')
    part_id = fields.Many2one('res.partner', "Partner", track_visibility='onchange')

    def print_report(self):
        out_invoice = self.env['account.move'].search(
            [('move_type', '=', 'out_invoice'), ('invoice_date', '>=', self.date_from),
             ('invoice_date', '<=', self.date_to)])
        in_invoice = self.env['account.move'].search(
            [('move_type', '=', 'in_invoice'), ('invoice_date', '>=', self.date_from),
             ('invoice_date', '<=', self.date_to)])
        in_and_out_invoice = self.env['account.move'].search(
            [('invoice_date', '>=', self.date_from), ('invoice_date', '<=', self.date_to)])
        data = []
        if self.part_id:
            if self.account_type in 'customer_invoices':
                for inv in out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids and inv.partner_id == self.part_id:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })

            elif self.account_type in 'supplier_invoices':
                for inv in in_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids and inv.partner_id == self.part_id:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })
            else:
                for inv in in_and_out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids and inv.partner_id == self.part_id:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })
        else:
            if self.account_type in 'customer_invoices':
                for inv in out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })

            elif self.account_type in 'supplier_invoices':
                for inv in in_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })
            else:
                for inv in in_and_out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })

        report_name = 'n2d_vat_report.vat_report'
        datas = {
            'ids': self._ids,
            'model': 'vat.report',
            'form': self.read()[0],
            'tax_data': data,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'account_type': self.account_type
        }
        if data:
            return (self.env['ir.actions.report'].search([('report_name', '=', report_name)], limit=1)
                    .report_action(self, data=datas))
        else:
            raise ValidationError("No Data Available!")

    def print_report_xlsx(self):
        out_invoice = self.env['account.move'].search(
            [('move_type', '=', 'out_invoice'), ('invoice_date', '>=', self.date_from),
             ('invoice_date', '<=', self.date_to)])
        in_invoice = self.env['account.move'].search(
            [('move_type', '=', 'in_invoice'), ('invoice_date', '>=', self.date_from),
             ('invoice_date', '<=', self.date_to)])
        in_and_out_invoice = self.env['account.move'].search(
            [('invoice_date', '>=', self.date_from), ('invoice_date', '<=', self.date_to)])
        data = []
        if self.part_id:
            if self.account_type in 'customer_invoices':
                for inv in out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids and inv.partner_id == self.part_id:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })

            elif self.account_type in 'supplier_invoices':
                for inv in in_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids and inv.partner_id == self.part_id:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })
            else:
                for inv in in_and_out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids and inv.partner_id == self.part_id:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })
        else:
            if self.account_type in 'customer_invoices':
                for inv in out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })

            elif self.account_type in 'supplier_invoices':
                for inv in in_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })
            else:
                for inv in in_and_out_invoice:
                    for line in inv.invoice_line_ids:
                        if line.tax_ids:
                            data.append({
                                'partner': inv.partner_id.name,
                                'trn': inv.partner_id.vat,
                                'date': inv.invoice_date,
                                'invoice': inv.name,
                                'vat_amount': inv.amount_tax,
                                'total_invoice': inv.amount_total,
                                'date_from': self.date_from,
                                'date_to': self.date_to,
                                'account_type': self.account_type,
                            })

        datas = {
            'ids': self._ids,
            'model': 'vat.report',
            'form': self.read()[0],
            'tax_data': data,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'account_type': self.account_type
        }
        if data:
            return self.env.ref('n2d_vat_report.report_vat_xlsx').report_action(self, data=datas)

        else:
            raise ValidationError("No Data Available!")



class VatXlsx(models.AbstractModel):
    _name = 'report.n2d_vat_report.vat_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, vat):
        sheet = workbook.add_worksheet('Vat')
        format_header = workbook.add_format({
            'bold': True,
            'font_size': 12,
            'align': 'center',
            'font': 'Arial',
            'bottom': False
        })
        content = workbook.add_format({
            'bold': False,
            'font_size': 10,
            'align': 'left',
            'font': 'Arial',
        })

        sheet.set_column('A:A', 20)
        sheet.set_column('B:B', 20)
        sheet.set_column('C:C', 20)
        sheet.set_column('D:D', 20)
        sheet.set_column('E:E', 20)
        sheet.set_column('F:F', 20)
        sheet.set_column('G:G', 20)
        row = 0
        col = 0
        sheet.write(row, col, 'Partner', format_header)
        sheet.write(row, col + 1, 'TRN', format_header)
        sheet.write(row, col + 2, 'Date', format_header)
        sheet.write(row, col + 3, 'Invoice', format_header)
        sheet.write(row, col + 4, 'VAT amount', format_header)
        sheet.write(row, col + 5, 'Total Invoice', format_header)
        for vat in data['tax_data']:
            row += 1
            sheet.write(row, col, vat['partner'], content)
            sheet.write(row, col + 1, vat['trn'], content)
            sheet.write(row, col + 2, vat['date'], content)
            sheet.write(row, col + 3, vat['invoice'], content)
            sheet.write(row, col + 4, vat['vat_amount'], content)
            sheet.write(row, col + 5, vat['total_invoice'], content)
        formula = f"=sum(E{2}:E{row+1})"
        row += 1
        sheet.write(row, col + 4, 'Total', format_header)
        row += 1
        sheet.write(row, col + 4, formula, content)
