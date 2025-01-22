# -*- coding: utf-8 -*-
from odoo import models, api


class order_report_xlsx(models.AbstractModel):
    _inherit = 'report.report_xlsx.abstract'
    _name = 'report.n2d_so_categ_inlines.order_report_doc_xlsx'

    @api.model
    def generate_xlsx_report(self, workbook, data, wizard):
        worksheet = workbook.add_worksheet("Order Report")
        bold = workbook.add_format(
            {'bold': True, 'bottom': True, 'right': True, 'left': True, 'top': True})

        hformat = workbook.add_format(
            {'bold': True, 'bottom': True, 'right': True, 'align': 'center', 'valign': 'center'})
        worksheet.write(0, 3, 'Order Report', bold)
        worksheet.write(3, 0, 'Date Form :', bold)
        worksheet.write(3, 1, str(wizard.date_from))

        worksheet.write(4, 0, 'Date To :', bold)
        worksheet.write(4, 1, str(wizard.date_to))

        worksheet.write(7, 0, 'DB Code/Action', hformat)
        worksheet.write(7, 1, 'TCR No.', hformat)
        worksheet.write(7, 2, 'PO No./Action', hformat)
        worksheet.write(7, 3, 'Site A', hformat)
        worksheet.write(7, 4, 'Region', hformat)
        worksheet.write(7, 5, 'Price list', hformat)
        worksheet.write(7, 6, 'Line', hformat)
        worksheet.write(7, 7, 'Description', hformat)
        worksheet.write(7, 8, 'Category', hformat)
        worksheet.write(7, 9, 'Qty', hformat)
        worksheet.write(7, 10, 'Unit Price', hformat)
        worksheet.write(7, 11, 'Total Unit price', hformat)
        worksheet.write(7, 12, 'Total Cost per Action', hformat)

        line_number = 8
        if wizard.status == 'done':
            domain = [('state', 'in', ['sale', 'done']),('confirmation_date', '>=', wizard.date_from), ('confirmation_date', '<=', wizard.date_to), ('confirmation_date', '<=', wizard.date_to)]
        else:
            domain = [('state', 'in', ['draft', 'sent']),('date_order', '>=', wizard.date_from), ('date_order', '<=', wizard.date_to),
                      ('date_order', '<=', wizard.date_to)]
        if wizard.tcr:
            domain.append(('tcr', 'ilike', wizard.tcr))
        if wizard.database_db:
            domain.append(('database_db', 'ilike', wizard.database_db))
        records = self.env['sale.order'].search(domain)

        for rec in records:


            if len(rec.order_line) > 1:
                cell_len = 'A'+ str(line_number+1) +':'+ 'A'+ str(line_number+len(rec.order_line))

                tot_cell_len = 'M'+ str(line_number+1) +':'+ 'M'+ str(line_number+len(rec.order_line))

                worksheet.merge_range(cell_len, rec.database_db or '', hformat)
                worksheet.merge_range(tot_cell_len, rec.amount_untaxed, hformat)
            else:
                worksheet.write(line_number, 0, rec.database_db or '', hformat)

                worksheet.write(line_number, 12, rec.amount_untaxed, hformat)


            for lin in rec.order_line:
                worksheet.write(line_number, 1, rec.tcr or '', hformat)



                worksheet.write(line_number, 2, ', '.join(map(lambda x: (x.name), lin.analytic_tag_ids)), hformat)
                worksheet.write(line_number, 3, rec.site_id or '', hformat)
                worksheet.write(line_number, 4, rec.analytic_account_id.region.name or '', hformat)
                worksheet.write(line_number, 5, rec.pricelist_id.name, hformat)

                worksheet.write(line_number, 6, lin.product_id.display_name, hformat)
                worksheet.write(line_number, 7, lin.name, hformat)
                worksheet.write(line_number, 8, lin.cate_id.display_name or '', hformat)
                worksheet.write(line_number, 9, lin.product_uom_qty, hformat)
                worksheet.write(line_number, 10, lin.price_unit, hformat)
                worksheet.write(line_number, 11, lin.price_subtotal, hformat)

                line_number += 1

