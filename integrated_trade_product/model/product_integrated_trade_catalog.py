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

from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model


class product_integrated_trade_catalog(Model):
    _name = 'product.integrated.trade.catalog'
    _auto = False
    _table = 'product_integrated_trade_catalog'

    # Fields Function Section
    def _get_customer_product_id(self, cr, uid, ids, name, arg, context=None):
        return {x: None for x in ids}

    def _set_customer_product_id(
            self, cr, uid, ids, field_name, field_value, arg, context):
        for pitc in self.browse(cr, uid, ids, context=context):
            pass
        #        psi = self.browse(cr, uid, ids, context=context)
        #        psi.write({'product_uom_stored': field_value})
        return True

    # Column Section
    _columns = {
        'product_id': fields.function(
            _get_customer_product_id, fnct_inv=_set_customer_product_id,
            string='Product', type='many2one',
            relation='product.product'),
        'supplier_product_name': fields.char(
            'Supplier Product Name', readonly='True'),
        'supplier_product_default_code': fields.char(
            'Supplier Product Code', readonly='True'),
        'supplier_partner_name': fields.char(
            'Supplier Partner Name', readonly='True'),
        'supplier_product_id': fields.many2one(
            'product.product', 'Supplier Product', readonly='True'),
        'supplier_company_id': fields.many2one(
            'res.company', 'Supplier Company', readonly='True'),
        'supplier_partner_id': fields.many2one(
            'res.partner', 'Supplier Partner', readonly='True'),
        'customer_company_id': fields.many2one(
            'res.company', 'Customer Company', readonly='True'),
    }

    # View Section
    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        cr.execute("""
CREATE OR REPLACE VIEW %s AS (
        SELECT
            pp.id as id,
            pp.id as supplier_product_id,
            pt.name as supplier_product_name,
            pp.default_code as supplier_product_default_code,
            rit.supplier_company_id,
            rit.supplier_partner_id,
            rit.customer_company_id,
            rit.customer_partner_id,
            rp.name as supplier_partner_name
        FROM product_product pp
        INNER JOIN product_template pt
            ON pp.product_tmpl_id = pt.id
        RIGHT JOIN res_integrated_trade rit
            ON pt.company_id = rit.supplier_company_id
        INNER JOIN res_partner rp
            ON rit.supplier_partner_id = rp.id
)""" % (self._table))
