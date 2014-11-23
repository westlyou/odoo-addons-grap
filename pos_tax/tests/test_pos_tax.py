# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Tax for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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


class TestPosTax(TransactionCase):
    """Tests for 'Point Of Sale - Tax' Module"""

    def setUp(self):
        super(TestPosTax, self).setUp()
        cr, uid = self.cr, self.uid

        # Get regitry
        self.imd_obj = self.registry('ir.model.data')
        self.ps_obj = self.registry('pos.session')
        self.po_obj = self.registry('pos.order')

        # Get ids from xml ids
        self.pc_id = self.imd_obj.get_object_reference(
            cr, uid, 'point_of_sale', 'pos_config_main')[1]
#        self.pp_obj = self.registry('product.product')
#        self.iarx_obj = self.registry('ir.actions.report.xml')
#        self.imd_obj = self.registry('ir.model.data')

    # Test Section
    def test_01_check_compute_tax(self):
        """Check the correct computation of a Pos Order"""
        cr, uid = self.cr, self.uid
        # Open a Session
        ps_id = self.ps_obj.create(cr, uid, {
            'config_id': self.pc_id,
        })
        self.ps_obj.open_cb(cr, uid, [ps_id])
        po_id = self.po_obj.create(cr, uid, {})
        po_id = po_id
#        cr, uid = self.cr, self.uid
#        pp_ids = self.pp_obj.search(cr, uid, [
#            ('pricetag_state', 'in', ('1', '2'))], context=None)
#        self.assertEqual(
#            len(pp_ids), self.ppw_obj._needaction_count(cr, uid),
#            "Incorrect computation of Needed Pricetag Quantity.")
