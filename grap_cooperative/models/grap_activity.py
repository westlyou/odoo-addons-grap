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


class GrapActivity(models.Model):
    _name = 'grap.activity'
    _inherits = {'grap.member': 'grap_member_id'}
    _order = 'activity_name'

    # Constant Section
    _GRAP_ACTIVITY_STATE = [
        ('draft', 'No linked'),
        ('progress', 'project in progress'),
        ('validated', 'Validated'),
        ('working', 'Working'),
        ('obsolete', 'project exited'),
    ]

#    name = fields.Char(compute='_compute_name_2', store=True)

    # Columns section
    grap_member_id = fields.Many2one(
        comodel_name='grap.member', string='Member', required=True,
        ondelete='cascade')

    activity_name = fields.Char('Activity Name', required=True)

    state = fields.Selection(
        selection=_GRAP_ACTIVITY_STATE, string='State', required=True,
        default='draft')

    code = fields.Char(string='code')

    siret = fields.Char('SIRET')

    vat = fields.Char('Taxe ID')

    web_site = fields.Char(string='Web Site')

    date_validated = fields.Date(string='Validation date by cooperative')

    date_in = fields.Date(
        string='Business In Date', help='Date of activity begins to work')

    date_out = fields.Date(
        string='Business Out Date', help='Date of activity ends to work')

    type_id = fields.Many2one(
        comodel_name='grap.type', string='Type')

    accountant_interlocutor_id = fields.Many2one(
        comodel_name='grap.people', string='Accoutant Interlocutor')

    hr_interlocutor_id = fields.Many2one(
        comodel_name='grap.people', string='Human Ressources Interlocutor')

    attendant_interlocutor_id = fields.Many2one(
        comodel_name='grap.people', string='Attendant Interlocutor')

    category_ids = fields.Many2many(
        comodel_name='grap.category', relation='grap_activity_category_rel',
        column1='activity_id', column2='category_id', string='Categories')

    people_ids = fields.One2many(
        comodel_name='grap.activity.people', inverse_name='activity_id',
        string='Workers')

    fte = fields.Float(
        compute='_compute_fte', string='Full Time Equivalent')

    # Compute Section
    @api.one
    @api.depends('people_ids', 'people_ids.fte')
    def _compute_fte(self):
        self.fte = 0
        for people in self.people_ids:
            self.fte += people.fte

    # Overload Section
    @api.model
    def create(self, vals):
        vals['name'] = vals.get('activity_name', False)
        return super(GrapActivity, self).create(vals)

    @api.one
    def write(self, vals):
        if vals.get('activity_name', False):
            vals['name'] = vals.get('activity_name')
        return super(GrapActivity, self).write(vals)

    # View section
    @api.one
    def button_state_previous(self):
        for index in range(len(self._GRAP_ACTIVITY_STATE) - 1):
            if self.state == self._GRAP_ACTIVITY_STATE[index + 1][0]:
                self.state = self._GRAP_ACTIVITY_STATE[index][0]
                break

    @api.one
    def button_state_next(self):
        for index in range(len(self._GRAP_ACTIVITY_STATE) - 1):
            if self.state == self._GRAP_ACTIVITY_STATE[index][0]:
                self.state = self._GRAP_ACTIVITY_STATE[index + 1][0]
                break
