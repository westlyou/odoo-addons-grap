# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Tax Module for Odoo
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)

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

from openerp.osv import fields
from openerp.osv.orm import Model


class pos_order_line(Model):
    _inherit = 'pos.order.line'

    # Columns section
    def _amount_line_all(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = dict([(i, {}) for i in ids])
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, [
                t.tax_id for t in line.pol_tax_rel_id], price, line.qty,
                line.product_id, line.order_id.partner_id)
            tax_amount = 0
            for t in taxes['taxes']:
                tax_amount += t['amount']
            cur = line.order_id.pricelist_id.currency_id
            res[line.id]['price_subtotal'] = cur_obj.round(
                cr, uid, cur, taxes['total'])
            res[line.id]['price_subtotal_incl'] = cur_obj.round(
                cr, uid, cur, taxes['total_included'])
            res[line.id]['tax_amount'] = cur_obj.round(
                cr, uid, cur, tax_amount)
        return res

    _columns = {
        'pol_tax_rel_id': fields.one2many(
            'pos.order.line.tax.rel', 'orderline_id',
            string='Tax Relation Id'),
        # Existing Fields 'price_subtotal' and 'price_subtotal_incl'
        'price_subtotal': fields.function(
            _amount_line_all, multi='pos_order_line_amount',
            string='Subtotal w/o Tax', store=True),
        'price_subtotal_incl': fields.function(
            _amount_line_all, multi='pos_order_line_amount', string='Subtotal',
            store=True),
        # New field 'tax_amount'
        'tax_amount': fields.function(
            _amount_line_all, multi='pos_order_line_amount',
            string='Tax Amount', store=True),
    }
