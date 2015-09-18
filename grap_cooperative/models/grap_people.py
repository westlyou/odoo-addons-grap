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


class GrapPeople(models.Model):
    _name = 'grap.people'
    _inherits = {'grap.member': 'grap_member_id'}
    _order = 'last_name, first_name'

    # Column section
    grap_member_id = fields.Many2one(
        comodel_name='grap.member', string='Member', required=True,
        ondelete='cascade')

    first_name = fields.Char(string='First name', required=True)

    last_name = fields.Char(string='Last name', required=True)

    private_phone = fields.Char(string='Private Phone')

    activity_ids = fields.One2many(
        comodel_name='grap.activity.people', inverse_name='people_id',
        string='Activities', readonly=True)

    accountant_activity_ids = fields.One2many(
        comodel_name='grap.activity',
        inverse_name='accountant_interlocutor_id',
        string='Accounting Performed for Activities')

    hr_activity_ids = fields.One2many(
        comodel_name='grap.activity', inverse_name='hr_interlocutor_id',
        string='Human Ressources Performed for Activities')

    attendant_activity_ids = fields.One2many(
        comodel_name='grap.activity', inverse_name='attendant_interlocutor_id',
        string='Attending Performed for Activities')

    mandate_ids = fields.Many2many(
        comodel_name='grap.mandate', relation='grap_people_mandate_rel',
        column1='people_id', column2='mandate_id', string='Mandates')

    description = fields.Text(string='Self Description')

    skills = fields.Text(string='Skills')

    catchword = fields.Char(string='Catchword')

    # Overload Section
    @api.model
    def create(self, vals):
        vals['name'] =\
            vals.get('last_name', '') + ' ' + vals.get('first_name', '')
        return super(GrapPeople, self).create(vals)

    @api.one
    def write(self, vals):
        if vals.get('first_name', False) and vals.get('last_name', False):
            vals['name'] =\
                vals.get('last_name', '') + ' ' + vals.get('first_name', '')
        elif vals.get('last_name', False):
            vals['name'] = \
                vals.get('last_name', '') + ' ' + self.first_name
        elif vals.get('first_name', False):
            vals['name'] = \
                self.last_name + ' ' + vals.get('first_name', '')
        return super(GrapPeople, self).write(vals)
