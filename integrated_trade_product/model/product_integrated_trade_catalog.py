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

from datetime import date

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields
from openerp.osv.orm import Model


class product_integrated_trade_catalog(Model):
    _name = 'product.integrated.trade.catalog'
    _auto = False
    _table = 'product_integrated_trade_catalog'



    # Overloadable Section
    def prepare_product_supplierinfo(
            self, cr, uid, supplier_partner_id, supplier_product_id,
            customer_company_id, customer_partner_id, context=None):
        """Overload this function to change the datas of the supplierinfo
        create when a link between a two products is done."""
        pp_obj = self.pool['product.product']
        rp_obj = self.pool['res.partner']
        ppl_obj = self.pool['product.pricelist']
        pp = pp_obj.browse(
            cr, SUPERUSER_ID, supplier_product_id, context=context)
        rp = rp_obj.browse(
            cr, SUPERUSER_ID, supplier_partner_id, context=context)
        price = ppl_obj.price_get(
            cr, uid, [rp.property_product_pricelist.id], pp.id,
            1.0, rp.id, {
                'uom': pp.uos_id.id,
                'date': date.today().strftime('%Y-%m-%d'),
            })[rp.property_product_pricelist.id]
        return {
            'min_qty': 0.0,
            'name': rp.id,
            'product_name': pp.name,
            'product_code': pp.default_code,
            'company_id': customer_company_id,
            'supplier_product_id': pp.id,
            'pricelist_ids': [[0, False, {
                'min_quantity': 0.0,
                'price': price}]],
        }

    # Public Function
    def update_product(
            self, cr, uid, pitc_ids, context=None):
        """Call this function to force to update product supplierinfo
        if it is necessary"""
        psi_obj = self.pool['product.supplierinfo']
        for pitc in self.browse(cr, uid, pitc_ids, context=context):
            import pdb; pdb.set_trace()
            psi_obj.unlink(
                cr, uid, [pitc.hidden_supplierinfo_id.id],
                context=context)
            pitc._link_product(
                cr, uid, pitc, pitc.customer_product_tmpl_id.id,
                context=context)

    # Private Section
    def _link_product(
            self, cr, uid, pitc, new_product_tmpl_id, context=None):
        psi_obj = self.pool['product.supplierinfo']
        vals = self.prepare_product_supplierinfo(
            cr, uid, pitc.supplier_partner_id.id, pitc.supplier_product_id.id,
            pitc.customer_company_id.id, pitc.customer_partner_id.id,
            context=context)
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

    # Column Section
    _columns = {
        'product_tmpl_id': fields.function(
            _get_product_tmpl_id, fnct_inv=_set_product_tmpl_id,
            string='Product', type='many2one',
            relation='product.template'),
        'customer_purchase_price': fields.float(
            'Customer Purchase Price', readonly=True),
        'supplier_product_name': fields.char(
            'Supplier Product Name', readonly=True),
        'supplier_product_default_code': fields.char(
            'Supplier Product Code', readonly=True),
        'supplier_partner_name': fields.char(
            'Supplier Partner Name', readonly=True),
        'hidden_product_tmpl_id': fields.many2one(
            'product.template', 'Product (Technical Field)', readonly=True),
        'hidden_supplierinfo_id': fields.many2one(
            'product.suppplierinfo', 'SupplierInfo (Technical Field)',
            readonly=True),
        'supplier_product_id': fields.many2one(
            'product.product', 'Supplier Product', readonly=True),
        'supplier_company_id': fields.many2one(
            'res.company', 'Supplier Company', readonly=True),
        'supplier_partner_id': fields.many2one(
            'res.partner', 'Supplier Partner', readonly=True),
        'customer_company_id': fields.many2one(
            'res.company', 'Customer Company', readonly=True),
        'customer_partner_id': fields.many2one(
            'res.partner', 'Customer Partner', readonly=True),
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
            c_psi.id as hidden_supplierinfo_id,
            c_psi.product_id as hidden_product_tmpl_id,
            c_psi.integrated_price as customer_purchase_price,
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
