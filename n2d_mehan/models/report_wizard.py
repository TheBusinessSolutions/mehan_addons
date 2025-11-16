# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class MehanTotalReportWizard(models.TransientModel):
    _name = 'mehan.total.report.wizard'
    _description = 'Total Injured & Death Report Wizard'

    report_type = fields.Selection([
        ('injured', 'Total Injured'),
        ('dead', 'Total Death'),
        ('both', 'Both')
    ], string='Report to Show', required=True, default='dead')
    
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To', default=fields.Date.today)
    
    # Optional filters
    committee_id = fields.Many2one('mehan.committee', string='Committee')
    year_finance_id = fields.Many2one('mehan.year.finance', string='Financial Year')
    work_place_id = fields.Many2one('work.place', string='Work Place')
    tag_id = fields.Many2one('work.place.tag', string='Work Place Tag')

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for rec in self:
            if rec.date_from and rec.date_to and rec.date_from > rec.date_to:
                raise ValidationError(_("Date From cannot be later than Date To"))

    def action_generate_report(self):
        """Generate the report based on selected type"""
        self.ensure_one()
        
        _logger.info("=== WIZARD STARTED ===")
        _logger.info("Report Type: %s", self.report_type)
        
        # Build domain based on filters
        domain = []
        
        if self.report_type == 'injured':
            domain.append(('member_type', '=', 'injured'))
        elif self.report_type == 'dead':
            domain.append(('member_type', '=', 'dead'))
        
        if self.date_from:
            domain.append(('create_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('create_date', '<=', self.date_to))
        if self.committee_id:
            domain.append(('committee_id', '=', self.committee_id.id))
        if self.work_place_id:
            domain.append(('work_place_id', '=', self.work_place_id.id))
        if self.tag_id:
            domain.append(('tag_id', '=', self.tag_id.id))

        _logger.info("Domain: %s", domain)
        
        # Get records
        records = self.env['deceased.info'].search(domain)
        
        _logger.info("Records found: %s", len(records))
        _logger.info("Record IDs: %s", records.ids)
        
        if not records:
            raise ValidationError(_("No records found for the selected criteria"))

        # For now, only handle death report
        if self.report_type == 'dead':
            _logger.info("Calling report with IDs: %s", records.ids)
            
            # Call the report directly
            return {
                'type': 'ir.actions.report',
                'report_name': 'n2d_mehan.report_mehan_total_death',
                'report_type': 'qweb-pdf',
                'report_file': 'n2d_mehan.report_mehan_total_death',
                'data': {
                    'date_from': str(self.date_from) if self.date_from else '',
                    'date_to': str(self.date_to) if self.date_to else '',
                },
                'context': {
                    'active_model': 'deceased.info',
                    'active_ids': records.ids,
                }
            }
        else:
            raise ValidationError(_("Only 'Total Death' report is implemented. Please select that option."))

    def action_open_tree_view(self):
        """Alternative: Open tree view instead of PDF report"""
        self.ensure_one()
        
        _logger.info("=== TREE VIEW ACTION ===")
        _logger.info("Report Type: %s", self.report_type)
        
        domain = [('state', '=', 'certified')]  # Filter only certified records
        
        if self.report_type == 'injured':
            domain.append(('member_type', '=', 'injured'))
        elif self.report_type == 'dead':
            domain.append(('member_type', '=', 'dead'))
        
        if self.date_from:
            domain.append(('create_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('create_date', '<=', self.date_to))
        if self.committee_id:
            domain.append(('committee_id', '=', self.committee_id.id))
        if self.work_place_id:
            domain.append(('work_place_id', '=', self.work_place_id.id))
        if self.tag_id:
            domain.append(('tag_id', '=', self.tag_id.id))
        
        _logger.info("Tree view domain: %s", domain)

        return {
            'name': _('Total Report: %s (Certified Only)') % dict(self._fields['report_type'].selection).get(self.report_type),
            'type': 'ir.actions.act_window',
            'res_model': 'deceased.info',
            'view_mode': 'tree,form',
            'domain': domain,
            'context': {
                'search_default_group_by_member_type': 1,
                'create': False,  # Disable create from this view
            },
        }