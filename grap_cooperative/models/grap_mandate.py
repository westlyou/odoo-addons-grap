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


class GrapMandate(models.Model):
    _name = 'grap.mandate'

    # Column Section
    name = fields.Char(required=True, string='Name')

    people_ids = fields.Many2many(
        comodel_name='grap.people', relation='grap_people_mandate_rel',
        column1='mandate_id', column2='people_id', string='Members')

    people_count = fields.Integer(
        compute='_compute_people_count', string='People count')

    # Compute Section
    @api.one
    @api.depends('people_ids')
    def _compute_people_count(self):
        self.people_count = len(self.people_ids)
