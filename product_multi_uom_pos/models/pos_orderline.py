# -*- coding: utf-8 -*-

##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2018-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: LINTO C T(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <https://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import _
from odoo.tools import float_is_zero
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class PosOrderLinesExtended(models.Model):
    _inherit = 'pos.order.line'

    uom_id = fields.Many2one('uom.uom', string="UOM")

    @api.model
    def create(self, values):
        """updating uom to orderlines"""
        _logger.info("values: %s", values)
        try:
            if values.get('uom_id'):
                values['uom_id'] = values['uom_id'][0]
        except Exception:
            values['uom_id'] = None
            pass
        res = super(PosOrderLinesExtended, self).create(values)
        return res


class PosOrderExtended(models.Model):
    _inherit = 'pos.order'

    # overwriting this function because, we need to set the uom id based on the unit
    # in the orderline instead of product uom, at the time of creating the stock moves
    def _create_order_picking(self):
        for order in self:
            for line in order.lines.filtered(lambda l: l.product_id.type in ['product', 'consu'] and not float_is_zero(l.qty, precision_rounding=l.product_id.uom_id.rounding)):    
                line.qty = line.qty*line.uom_id.ratio
        
        super(PosOrderExtended, self)._create_order_picking()
        
        
class ProductTemplateExtended(models.Model):
    _inherit = 'product.template'
    
    def get_po_uom(self):
        uom_po_id = [self.uom_po_id.id, self.uom_po_id.display_name, [self.uom_po_id.category_id.id]]
        _logger.info("returning Purchase UoM to POS GUI %s", uom_po_id)
        return uom_po_id
            
