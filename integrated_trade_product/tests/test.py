# -*- encoding: utf-8 -*-
##############################################################################
#
#    Integrated Trade - Base module for OpenERP
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

from openerp.tests.common import TransactionCase


class Test(TransactionCase):

    # Overload Section
    def setUp(self):
        super(Test, self).setUp()

        # Get Registries
        self.imd_obj = self.registry('ir.model.data')
        self.pitc_obj = self.registry('product.integrated.trade.catalog')
        self.pp_obj = self.registry('product.product')

        # Get ids from xml_ids
        self.supplier_apple_id = self.imd_obj.get_object_reference(
            self.cr, self.uid,
            'integrated_trade_product', 'product_supplier_apple')[1]
        self.customer_apple_id = self.imd_obj.get_object_reference(
            self.cr, self.uid,
            'integrated_trade_product', 'product_customer_apple')[1]

    # Test Section
    def test_01_product_assocation(self):
        """[Functional Test] Check if associate a product create a
        product supplierinfo"""
        cr, uid = self.cr, self.uid
        pitc_id = self.pitc_obj.search(cr, uid, [
            ('supplier_product_id', '=', self.supplier_apple_id),
        ])
        self.pitc_obj.write(cr, uid, [pitc_id], {
            'product_id': self.customer_apple_id})
        pp = self.pp_obj.browse(
            cr, uid, self.customer_apple_id)
        self.assertEqual(
            len(pp.seller_ids), 1,
            """Associate a Customer Product to a Supplier Product must"""
            """ create a Product Supplierinfo.""")
