# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point of Sale - Remove Default Partner module for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
#    @author Julien WESTE
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

from openerp.osv.orm import Model


class pos_order(Model):
    _inherit = 'pos.order'

    def default_get(self, cr, uid, fields_list, context=None):
        if context is None:
            context = {}
        if context.get("default_partner_id", False):
            del context["default_partner_id"]
        return super(pos_order, self).default_get(
            cr, uid, fields_list, context=context)