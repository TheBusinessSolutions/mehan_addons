# -*- encoding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class AssetQrcodeWizard(models.TransientModel):
    _name = 'asset.qr.wizard'

    asset_ids = fields.Many2many('bt.asset', 'asset_wiz_rel', 'wiz', 'asset')


    def get_data(self):
        self.ensure_one()
        if self.asset_ids:
            assets = self.env['bt.asset'].search_read(domain=[('id', 'in', self.asset_ids.ids)])
            data = {
                'assets': assets
            }
            print(data)
            return self.env.ref('bt_asset_management.action_report_asset_qr').report_action(self, data=data)

