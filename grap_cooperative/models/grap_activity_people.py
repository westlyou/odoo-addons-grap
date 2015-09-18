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

from openerp import fields, models, api
from openerp.tools.translate import _


class GrapActivityPeople(models.Model):
    _name = 'grap.activity.people'
    _order = 'people_id'

    # Columns section
    name = fields.Char(
        compute='_compute_name', string='Name', store=True)

    activity_id = fields.Many2one(
        comodel_name='grap.activity', string='Activity', required=True,
        ondelete='cascade', readonly=True)

    people_id = fields.Many2one(comodel_name='grap.people', string='People')

    fte = fields.Float(string='Full Time Equilalent', required=True, default=1)

    working_email = fields.Char(
        related='people_id.working_email', string='Contact EMail')

    private_phone = fields.Char(
        related='people_id.private_phone', string='Private Phone')

    working_phone = fields.Char(
        related='people_id.grap_member_id.working_phone',
        string='Working Phone')

    # Compute Section
    @api.one
    @api.depends('activity_id', 'activity_id.name', 'fte')
    def _compute_name(self):
        self.name = _(
            '%s (%d FTE)') % (self.activity_id.name, self.fte)

    # Constraints section
    _sql_constraints = [
        (
            'activity_people_uniq',
            'unique(activity_id, people_id)',
            'A people can work only once time in an activity!'),
    ]
