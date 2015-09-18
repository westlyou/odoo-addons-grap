# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Cooperative module for Odoo
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

from openerp import models, fields, api


class GrapCollege(models.Model):
    _name = 'grap.college'

    # Columns section
    name = fields.Char(string='Name', required=True)

    percentage = fields.Integer(string='Percentage', required=True)

    member_ids = fields.One2many(
        comodel_name='grap.member', inverse_name='college_id',
        string='Members')

    member_count = fields.Integer(
        compute='_compute_member_count', string='Members count')

    # Field Function section
    @api.one
    @api.depends('member_ids')
    def _compute_member_count(self):
        self.member_count = len(self.member_ids)
