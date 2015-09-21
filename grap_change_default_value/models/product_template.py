# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Default Value Module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
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

from openerp import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Default Section
    @api.model
    def _get_uom_id(self):
        if self._context.get('install_mode', False):
            return super(ProductTemplate, self)._get_uom_id()
        else:
            return False

    # Column Section
    uom_id = fields.Many2one(default=_get_uom_id)

    uom_po_id = fields.Many2one(default=_get_uom_id)
