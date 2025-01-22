# -*- encoding: utf-8 -*-

{
    "name": "Inventory Customization",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "Specific Industry Applications",
    "depends": [
        'stock',
    ],
    "data": [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/stock_inventory_view.xml',
        'views/stock_scrap_batch_view.xml',
        'views/stock.picking_view.xml',
        # 'reports/inventory_reports_inherit.xml'
    ],
}
