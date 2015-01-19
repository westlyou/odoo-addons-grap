# -*- encoding: utf-8 -*-
##############################################################################
#
#    Integrated Trade - Product module for OpenERP
#    Copyright (C) 2014-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
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

from openerp import SUPERUSER_ID
from openerp.osv.orm import Model


class res_partner(Model):
    _inherit = 'res.partner'

    # Public Function
    def update_all_products_as_customer(self, cr, uid, ids, context=None):
        """ Update all product.pricelistinfo of products template that are
        linked to external products for defined customers"""
        pitc_obj = self.pool['product.integrated.trade.catalog']
        pitc_ids = pitc_obj.search(cr, SUPERUSER_ID, [
            ('customer_partner_id', 'in', ids)], context=context)
        pitc_obj = self.update_product(cr, uid, pitc_ids, context=context)

# TODO a voir si utile.
#    def update_all_products_as_supplier(self, cr, uid, ids, context=None):
#        pitc_obj = self.pool['product.integrated.trade.catalog']
#        pitc_ids = pitc_obj.search(cr, SUPERUSER_ID, [
#            ('supplier_partner_id', 'in', ids)], context=context)
#        pitc_obj = self.update_product(cr, uid, pitc_ids, context=context)
