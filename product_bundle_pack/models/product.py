# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
import math
from odoo import api, fields, models, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo import SUPERUSER_ID
from odoo.tools.float_utils import float_round



class ProductPack(models.Model):
	_name = 'product.pack'
	_description = "Product Pack"
	
	product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True)
	qty_uom = fields.Float(string='Quantity', required=True, default=1.0)
	bi_product_template = fields.Many2one(comodel_name='product.template', string='Product pack')
	bi_image = fields.Binary(related='product_id.image_1920', string='Image', store=True)
	price = fields.Float(related='product_id.lst_price', string='Product Price')
	uom_id = fields.Many2one(related='product_id.uom_id' , string="Unit of Measure", readonly="1")
	name = fields.Char(related='product_id.name', readonly="1")


class ProductTemplate(models.Model):
	_inherit = 'product.template'

	is_pack = fields.Boolean(string='Is Product Pack')
	cal_pack_price = fields.Boolean(string='Calculate Pack Price')
	pack_ids = fields.One2many(comodel_name='product.pack', inverse_name='bi_product_template', string='Product pack')

	@api.model
	def create(self,vals):
		total = 0
		res = super(ProductTemplate,self).create(vals)
		if res.cal_pack_price:
			if 'pack_ids' in vals or 'cal_pack_price' in vals:
					for pack_product in res.pack_ids:
							qty = pack_product.qty_uom
							price = pack_product.product_id.list_price
							total += qty * price
		if total > 0:
			res.list_price = total
		return res


	def write(self,vals):
		total = 0
		res = super(ProductTemplate, self).write(vals)
		for pk in self:
			if pk.cal_pack_price:
				if 'pack_ids' in vals or 'cal_pack_price' in vals:
					for pack_product in pk.pack_ids:
						qty = pack_product.qty_uom
						price = pack_product.product_id.list_price
						total += qty * price

		if total > 0:
			self.list_price = total
		return res


	def _compute_quantities_dict(self):
		# TDE FIXME: why not using directly the function fields ?
		variants_available = {
			p['id']: p for p in self.product_variant_ids.read(['qty_available', 'virtual_available', 'incoming_qty', 'outgoing_qty'])
		}
		prod_available = {}
		for template in self:
			qty_available = 0
			virtual_available = 0
			incoming_qty = 0
			outgoing_qty = 0
			if template.is_pack == True:
				qty_available = 0.0
				virtual_available = 0.0
				for pid in template.pack_ids.filtered(lambda x : x.product_id.type == 'product'):
					if not pid.qty_uom == 0.0:
						temp = math.floor(pid.product_id.qty_available / pid.qty_uom)
						temp2 = math.floor(pid.product_id.virtual_available/ pid.qty_uom)
						
						if qty_available == 0.0:
							qty_available = temp
						elif qty_available < temp:
							qty_available = qty_available
						elif temp < qty_available:
							qty_available = temp

						if virtual_available == 0.0:
							virtual_available = temp2
						elif virtual_available < temp2:
							virtual_available = virtual_available
						elif temp2 < virtual_available:
							virtual_available = temp2
					else:
						qty_available = 0.0
						virtual_available = 0.0

					incoming_qty += pid.product_id.incoming_qty			
					outgoing_qty += pid.product_id.outgoing_qty

				qty_available = qty_available
				virtual_available = virtual_available
				prod_available[template.id] = {
					"qty_available": qty_available,
					"virtual_available": virtual_available,
					"incoming_qty": incoming_qty,
					"outgoing_qty": outgoing_qty,
				}
				search_line = self.env['stock.quant'].search([('product_id.product_tmpl_id','=',template.id)])
				if search_line :
					for stock_line_id in search_line :
						stock_line_id.write({'inventory_quantity' :qty_available})
						stock_line_id._compute_inventory_diff_quantity()
						stock_line_id.action_apply_inventory()

			else:
				for p in template.product_variant_ids:
					qty_available += variants_available[p.id]["qty_available"]
					virtual_available += variants_available[p.id]["virtual_available"]
					incoming_qty += variants_available[p.id]["incoming_qty"]
					outgoing_qty += variants_available[p.id]["outgoing_qty"]
				prod_available[template.id] = {
				"qty_available": qty_available,
				"virtual_available": virtual_available,
				"incoming_qty": incoming_qty,
				"outgoing_qty": outgoing_qty,
			}
		return prod_available


class PurchaseOrder(models.Model):
	_inherit = 'purchase.order'		

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	allow_bundle = fields.Boolean('Allow Manual Dropshipping Delivery')

	def get_values(self):
		res = super(ResConfigSettings, self).get_values()
		allow_bundle = self.env['ir.config_parameter'].sudo().get_param('product_bundle_pack.allow_bundle')
		res.update(
			allow_bundle = allow_bundle,
		)
		return res

	def set_values(self):
		super(ResConfigSettings, self).set_values()
		self.env['ir.config_parameter'].sudo().set_param('product_bundle_pack.allow_bundle', self.allow_bundle)


class ProductProduct(models.Model):
	_inherit = 'product.product'

	def _compute_quantities_dict(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
		domain_quant_loc, domain_move_in_loc, domain_move_out_loc = self._get_domain_locations()
		domain_quant = [('product_id', 'in', self.ids)] + domain_quant_loc
		dates_in_the_past = False
		# only to_date as to_date will correspond to qty_available
		to_date = fields.Datetime.to_datetime(to_date)
		if to_date and to_date < fields.Datetime.now():
			dates_in_the_past = True

		domain_move_in = [('product_id', 'in', self.ids)] + domain_move_in_loc
		domain_move_out = [('product_id', 'in', self.ids)] + domain_move_out_loc
		if lot_id is not None:
			domain_quant += [('lot_id', '=', lot_id)]
		if owner_id is not None:
			domain_quant += [('owner_id', '=', owner_id)]
			domain_move_in += [('restrict_partner_id', '=', owner_id)]
			domain_move_out += [('restrict_partner_id', '=', owner_id)]
		if package_id is not None:
			domain_quant += [('package_id', '=', package_id)]
		if dates_in_the_past:
			domain_move_in_done = list(domain_move_in)
			domain_move_out_done = list(domain_move_out)
		if from_date:
			date_date_expected_domain_from = [('date', '<=', from_date)]
			domain_move_in += date_date_expected_domain_from
			domain_move_out += date_date_expected_domain_from
		if to_date:
			date_date_expected_domain_to = [('date', '<=', to_date)]
			domain_move_in += date_date_expected_domain_to
			domain_move_out += date_date_expected_domain_to

		Move = self.env['stock.move'].with_context(active_test=False)
		Quant = self.env['stock.quant'].with_context(active_test=False)
		domain_move_in_todo = [('state', 'in',
								('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_in
		domain_move_out_todo = [('state', 'in',
								 ('waiting', 'confirmed', 'assigned', 'partially_available'))] + domain_move_out
		moves_in_res = dict((item['product_id'][0], item['product_qty']) for item in
							Move.read_group(domain_move_in_todo, ['product_id', 'product_qty'], ['product_id'],
											orderby='id'))
		moves_out_res = dict((item['product_id'][0], item['product_qty']) for item in
							 Move.read_group(domain_move_out_todo, ['product_id', 'product_qty'], ['product_id'],
											 orderby='id'))
		quants_res = dict((item['product_id'][0], (item['quantity'], item['reserved_quantity'])) for item in
						  Quant.read_group(domain_quant, ['product_id', 'quantity', 'reserved_quantity'],
										   ['product_id'], orderby='id'))
		if dates_in_the_past:
			# Calculate the moves that were done before now to calculate back in time (as most questions will be recent ones)
			domain_move_in_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_in_done
			domain_move_out_done = [('state', '=', 'done'), ('date', '>', to_date)] + domain_move_out_done
			moves_in_res_past = dict((item['product_id'][0], item['product_qty']) for item in
									 Move.read_group(domain_move_in_done, ['product_id', 'product_qty'], ['product_id'],
													 orderby='id'))
			moves_out_res_past = dict((item['product_id'][0], item['product_qty']) for item in
									  Move.read_group(domain_move_out_done, ['product_id', 'product_qty'],
													  ['product_id'], orderby='id'))

		res = dict()
		for product in self.with_context(prefetch_fields=False):
			product_id = product.id
			if not product_id:
				res[product_id] = dict.fromkeys(
					['qty_available', 'free_qty', 'incoming_qty', 'outgoing_qty', 'virtual_available'],
					0.0,
				)
				continue
			rounding = product.uom_id.rounding
			res[product_id] = {}
			if product.is_pack == True:
				qty_available = 0.0
				incoming_qty = 0.0
				outgoing_qty = 0.0
				virtual_available = 0.0
				for pid in product.pack_ids.filtered(lambda x : x.product_id.type == 'product'):
					if not pid.qty_uom == 0.0:	
						temp_avail = math.floor(pid.product_id.qty_available / pid.qty_uom)
						if qty_available == 0.0:
							qty_available = temp_avail
						elif qty_available < temp_avail:
							qty_available = qty_available
						elif temp_avail < qty_available:
							qty_available = temp_avail

						temp_incoming = math.floor(pid.product_id.incoming_qty / pid.qty_uom)
						if incoming_qty == 0.0:
							incoming_qty = temp_incoming
						elif incoming_qty < temp_incoming:
							incoming_qty = incoming_qty
						elif temp_incoming < incoming_qty:
							incoming_qty = temp_incoming

						temp_outgoing = math.floor(pid.product_id.outgoing_qty / pid.qty_uom)
						if outgoing_qty == 0.0:
							outgoing_qty = temp_outgoing
						elif outgoing_qty < temp_outgoing:
							outgoing_qty = outgoing_qty
						elif temp_outgoing < outgoing_qty:
							outgoing_qty = temp_outgoing

						temp_virtual = math.floor(pid.product_id.virtual_available / pid.qty_uom)
						if virtual_available == 0.0:
							virtual_available = temp_virtual
						elif virtual_available < temp_virtual:
							virtual_available = virtual_available
						elif temp_virtual < virtual_available:
							virtual_available = temp_virtual
					else:
						qty_available = 0.0
						incoming_qty = 0.0
						outgoing_qty = 0.0
						virtual_available = 0.0
				
				qty_available = qty_available
				incoming_qty = incoming_qty
				outgoing_qty = outgoing_qty
				virtual_available = virtual_available
				reserved_quantity = quants_res.get(product_id, [False, 0.0])[1]
				res[product.id]['qty_available'] = float_round(qty_available, precision_rounding=product.uom_id.rounding)
				res[product_id]['free_qty'] = float_round(qty_available - reserved_quantity, precision_rounding=rounding)
				res[product.id]['incoming_qty'] = float_round(incoming_qty, precision_rounding=product.uom_id.rounding)
				res[product.id]['outgoing_qty'] = float_round(outgoing_qty, precision_rounding=product.uom_id.rounding)
				res[product.id]['virtual_available'] = float_round(virtual_available, precision_rounding=product.uom_id.rounding)
				search_line = self.env['stock.quant'].search([('product_id','=',product.id)])
				if search_line :
					for stock_line_id in search_line :
						stock_line_id.write({'inventory_quantity' :qty_available})
						stock_line_id._compute_inventory_diff_quantity()
						stock_line_id.action_apply_inventory()
				else:
					company_user = self.env.company
					warehouse = self.env['stock.warehouse'].search([('company_id', '=', company_user.id)], limit=1)

					product_uom_id=self.env['product.product'].browse(product.id).uom_id
					stock_line_id = self.env['stock.quant'].create({'product_id':product.id, 'product_uom_id' : product_uom_id.id  ,'inventory_quantity': qty_available,'location_id':warehouse.lot_stock_id.id})
					stock_line_id._compute_inventory_diff_quantity()
					stock_line_id.action_apply_inventory()
			
			else:
				if dates_in_the_past:
					qty_available = quants_res.get(product_id, [0.0])[0] - moves_in_res_past.get(product_id, 0.0) + moves_out_res_past.get(product_id, 0.0)
				else:
					qty_available = quants_res.get(product_id, [0.0])[0]
				reserved_quantity = quants_res.get(product_id, [False, 0.0])[1]
				res[product_id]['qty_available'] = float_round(qty_available, precision_rounding=rounding)
				res[product_id]['free_qty'] = float_round(qty_available - reserved_quantity, precision_rounding=rounding)
				res[product_id]['incoming_qty'] = float_round(moves_in_res.get(product_id, 0.0), precision_rounding=rounding)
				res[product_id]['outgoing_qty'] = float_round(moves_out_res.get(product_id, 0.0), precision_rounding=rounding)
				res[product_id]['virtual_available'] = float_round(
					qty_available + res[product_id]['incoming_qty'] - res[product_id]['outgoing_qty'],
					precision_rounding=rounding)

		return res