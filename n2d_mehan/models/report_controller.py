# -*- coding: utf-8 -*-

from odoo import models, api


class MehanTotalReport(models.AbstractModel):
    _name = 'report.n2d_mehan.report_mehan_total'
    _description = 'Mehan Total Report Controller'

    @api.model
    def _get_report_values(self, docids, data=None):
        """
        Override to pass custom data to the report template
        """
        import logging
        _logger = logging.getLogger(__name__)
        
        # If docids is None, get from context
        if not docids:
            docids = self.env.context.get('active_ids', [])
        
        docs = self.env['deceased.info'].browse(docids)
        
        # Get data from wizard
        if not data:
            data = {}
            
        report_type = data.get('report_type', 'both')
        grouped_data = data.get('grouped_data', {})
        
        _logger.info("=== REPORT DEBUG ===")
        _logger.info("DocIDs: %s", docids)
        _logger.info("Docs count: %s", len(docs))
        _logger.info("Report Type: %s", report_type)
        _logger.info("Grouped Data: %s", grouped_data)
        _logger.info("===================")
        
        return {
            'doc_ids': docids,
            'doc_model': 'deceased.info',
            'docs': docs,
            'data': data,
            'report_type': report_type,
            'grouped_data': grouped_data,
            'date_from': data.get('date_from', ''),
            'date_to': data.get('date_to', ''),
            'year_finance': data.get('year_finance', ''),
        }