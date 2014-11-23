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

    # Overload Function
#    def _amount_line_all(self, cr, uid, ids, field_names, arg, context=None):
#        # Call Super function to be sure that this module is not incompatible
#        # with other module that could overload this function
#        res = super(pos_order_line, self)._amount_line_all(
#            cr, uid, ids, field_names, arg, context=context)
#        at_obj = self.pool['account.tax']
#        for pol in self.browse(cr, uid, ids, context=context):
#            # Recompute Taxes
#            at_ids = [
#                tax for tax in pol.product_id.taxes_id
#                if tax.company_id.id == pol.order_id.company_id.id]
#            price = pol.price_unit * (1 - (pol.discount or 0.0) / 100.0)
#            taxes = at_obj.compute_all(
#                cr, uid, at_ids, price, pol.qty, product=pol.product_id,
#                partner=pol.order_id.partner_id or False)
#            # Add field 'price_subototal_excl'
#            print taxes
#            res[pol.id]['price_subtotal_excl'] = 0
#        return res

    _columns = {
        'tax_ids': fields.many2many(
            'account.tax', 'pos_order_line_tax_rel',
            'order_line_id', 'tax_id',
            'Taxes', readonly=True,
        ),
#        'price_subtotal_excl': fields.function(
#            _amount_line_all, multi='pos_order_line_amount',
#            string='Subtotal Vat Excl.', store=True),
    }

    # View Section
    def onchange_product_id(
            self, cr, uid, ids, pricelist, product_id, qty=0, partner_id=False,
            order_id=False, context=None):
        print "onchange_product_id"
        context = context or {}
        if not product_id:
            return {}
        result = super(pos_order_line, self).onchange_product_id(
            cr, uid, ids, pricelist, product_id, qty=qty,
            partner_id=partner_id, context=context)
        at_obj = self.pool['account.tax']
        pp = self.pool['product.product']\
            .browse(cr, uid, product_id, context=context)
        ru = self.pool['res.users']\
            .browse(cr, uid, uid, context=context)
        print order_id
#        at_ids = [
#            tax for tax in pp.taxes_id
#            if tax.company_id.id == ru.company_id.id]
#        result['tax_ids'] = at_ids
        print result
        return result


#    def onchange_qty(
#            self, cr, uid, ids, product, discount, qty, price_unit,
#            context=None):
#        result = super(pos_order_line, self).onchange_qty(
#            cr, uid, ids, product, discount, qty, price_unit, context=context)
#        if not product:
#            return result

#        account_tax_obj = self.pool.get('account.tax')
#        product_obj = self.pool.get('product.product')
#        prod = product_obj.browse(cr, uid, product, context=context)

#        price = price_unit * (1 - (discount or 0.0) / 100.0)
#        taxes = account_tax_obj.compute_all(
#            cr, uid, prod.taxes_id, price, qty, product=prod, partner=False)
#        tax_values = []
#        for tax in taxes['taxes']:
#            tax_values.append((0, 0, {
#                'tax_id': tax['id'],
#                'baseHT': taxes['total'],
#                'amount_tax': tax['amount'],
#            }))
#        result['value']['pol_tax_rel_id'] = tax_values
        return result
