# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv.orm import TransientModel


class stock_fill_inventory(TransientModel):
    _inherit = 'stock.fill.inventory'

    # Overload Section
    def fill_inventory(self, cr, uid, ids, context=None):
        inventory_obj = self.pool['stock.inventory']
        res = super(stock_fill_inventory, self).fill_inventory(
            cr, uid, ids, context=context)

        # Fix price_unit to 0
        inventory_obj.reset_price_unit(
            cr, uid, context['active_ids'], context=context)
        return res
