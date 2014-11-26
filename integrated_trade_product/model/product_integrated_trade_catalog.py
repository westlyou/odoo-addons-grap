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
from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model


class product_integrated_trade_catalog(Model):
    _name = 'product.integrated.trade.catalog'
    _auto = False
    _table = 'product_integrated_trade_catalog'

    # Fields Function Section
    def _get_product_tmpl_id(self, cr, uid, ids, name, arg, context=None):
        res = {}
        for pitc in self.browse(cr, uid, ids, context=context):
            res[pitc.id] = pitc.hidden_product_tmpl_id.id
        return res

    def _set_product_tmpl_id(
            self, cr, uid, ids, field_name, field_value, arg, context=None):
        if not type(ids) is list:
            ids = [ids]
        for pitc in self.browse(cr, uid, ids, context=context):
            if field_value:
                self._unlink_customer_product_tmpl(
                    cr, uid, [field_value], context=context)
            self._unlink_supplier_product(
                cr, uid, [pitc.supplier_product_id.id], context=context)
            if field_value:
                self._link_product(
                    cr, uid, pitc, field_value,
                    context=context)
        return True

    def _prepare_product_supplierinfo(
            self, cr, uid, supplier_partner_id, supplier_product_id,
            customer_company_id, context=None):
        pp_obj = self.pool['product.product']
        rp_obj = self.pool['res.partner']
        rp = rp_obj.browse(
            cr, SUPERUSER_ID, supplier_partner_id, context=context)
        pp = pp_obj.browse(
            cr, SUPERUSER_ID, supplier_product_id, context=context)
        return {
            'min_qty': 0.0,
            'name': rp.id,
            'product_name': pp.name,
            'product_code': pp.default_code,
            'company_id': customer_company_id,
            'supplier_product_id': pp.id,
        }

    # Private Section
    def _link_product(
            self, cr, uid, pitc, new_product_tmpl_id, context=None):
        psi_obj = self.pool['product.supplierinfo']
        vals = self._prepare_product_supplierinfo(
            cr, uid, pitc.supplier_partner_id.id, pitc.supplier_product_id.id,
            pitc.customer_company_id.id, context=context)
        vals['product_id'] = new_product_tmpl_id
        psi_obj.create(cr, uid, vals, context=context)

    def _unlink_supplier_product(
            self, cr, uid, supplier_product_ids, context=None):
        psi_obj = self.pool['product.supplierinfo']
        res = psi_obj.search(cr, uid, [
            ('supplier_product_id', 'in', supplier_product_ids),
            ], context=context)
        psi_lst = psi_obj.browse(cr, uid, res, context=context)
        product_tmpl_ids = [x.product_id.id for x in psi_lst]
        self._unlink_customer_product_tmpl(
            cr, uid, product_tmpl_ids, context=context)

    def _unlink_customer_product_tmpl(
            self, cr, uid, customer_product_ids, context=None):
            """ FIXME: Maybe better to say to overload
            product_supplierinfo.unlink()
            Function to unlink a product associated to an supplier Product.
            Please Overload this function to add extra constraints, for
            exemple, disable the possibility to unlink a product if there
            is pending sale / purchase of that product."""
        psi_obj = self.pool['product.supplierinfo']
        res = psi_obj.search(cr, uid, [
        ('product_id', 'in', customer_product_ids)], context=context)
        psi_obj.unlink(cr, uid, res, context=context)
        return len(res)

    # Column Section
    _columns = {
        'product_tmpl_id': fields.function(
            _get_product_tmpl_id, fnct_inv=_set_product_tmpl_id,
            string='Product', type='many2one',
            relation='product.template'),
        'supplier_product_name': fields.char(
            'Supplier Product Name', readonly='True'),
        'supplier_product_default_code': fields.char(
            'Supplier Product Code', readonly='True'),
        'supplier_partner_name': fields.char(
            'Supplier Partner Name', readonly='True'),
        'hidden_product_tmpl_id': fields.many2one(
            'product.template', 'Product (Technical Field)', readonly='True'),
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
            s_pp.id as id,
            s_pp.id as supplier_product_id,
            s_pt.name as supplier_product_name,
            s_pp.default_code as supplier_product_default_code,
            c_psi.product_id as hidden_product_tmpl_id,
            rit.supplier_company_id,
            rit.supplier_partner_id,
            rit.customer_company_id,
            rit.customer_partner_id,
            c_rp.name as supplier_partner_name
        FROM product_product s_pp
        INNER JOIN product_template s_pt
            ON s_pp.product_tmpl_id = s_pt.id
        RIGHT JOIN res_integrated_trade rit
            ON s_pt.company_id = rit.supplier_company_id
        INNER JOIN res_partner c_rp
            ON rit.supplier_partner_id = c_rp.id
        LEFT JOIN product_supplierinfo c_psi
            ON c_psi.supplier_product_id = s_pp.id
)""" % (self._table))
