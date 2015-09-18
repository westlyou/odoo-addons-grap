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


class GrapTimesheetType(models.Model):
    _name = 'grap.timesheet.type'
#    _order = 'complete_name'

    # Columns section
    name = fields.Char(string='Name', required=True)

    active = fields.Boolean(string='Active', default=True)

    parent_id = fields.Many2one(
        comodel_name='grap.timesheet.type', string='Parent')

    display_name = fields.Char(
        compute='_compute_display_name', string='Complete Name', store=True)

    # Compute Section
    @api.one
    @api.depends('parent_id', 'name')
    def _compute_display_name(self):
        if self.parent_id:
            self.display_name =\
                self.parent_id.display_name + ' / ' + self.name
        else:
            self.display_name = self.name
