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

from openerp import models, fields, api


class GrapCategory(models.Model):
    _name = 'grap.category'

    # Columns section
    name = fields.Char(string='Name', required=True)

    activity_ids = fields.Many2many(
        comodel_name='grap.activity', relation='grap_activity_category_rel',
        column1='category_id', column2='activity_id', string='Activities')

    activity_count = fields.Integer(
        compute='_compute_activity_count', string='Activities count')

    # Compute section
    @api.one
    @api.depends('activity_ids')
    def _compute_activity_count(self):
        self.activity_count = len(self.activity_ids)
