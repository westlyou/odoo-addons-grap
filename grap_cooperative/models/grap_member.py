# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Cooperative module for Odoo
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

from openerp import models, fields


class GrapMember(models.Model):
    _name = 'grap.member'
    _order = 'name'

    # Columns section
    name = fields.Char(string='Name', required=True, readonly=True)

    image = fields.Binary(string='Image', help='Limited to 512x512px.')

    street = fields.Char(string='Street')

    zip = fields.Char(string='Zip')

    city = fields.Char(string='City')

    working_email = fields.Char(string='Contact EMail')

    working_phone = fields.Char(string='Working Phone')

    college_id = fields.Many2one(comodel_name='grap.college', string='College')

    date_capital_entry = fields.Date(string='Entry date In Capital')

    share_number = fields.Integer(string='Number of Share in Capital')
