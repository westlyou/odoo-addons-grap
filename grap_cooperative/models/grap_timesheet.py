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


class GrapTimesheet(models.Model):
    _name = 'grap.timesheet'
    _order = 'date desc, id desc'

    # Columns section
    name = fields.Char(string='Name', required=True, default='/')

    date = fields.Date(
        string='Date', required=True, default=fields.Date.context_today)

    amount = fields.Float(string='Worked Hours', required=True, default=0.0)

    worker_id = fields.Many2one(
        comodel_name='grap.people', string='Worker', required=True)

    activity_ids = fields.Many2many(
        comodel_name='grap.activity', relation='grap_timesheet_activity_rel',
        column1='timesheet_id', column2='activity_id', string='Activities',
        required=True)

    type_id = fields.Many2one(
        comodel_name='grap.timesheet.type', string='Work Type', required=True)

    timesheet_group_id = fields.Many2one(
        comodel_name='grap.timesheet.group', string='Group',
        compute='_compute_timesheet_group_id',
        inverse='_set_timesheet_group_id')

    activity_qty = fields.Integer(
        compute='_compute_activity_info', string='Activities Quantity',
        multi='activity')

    amount_per_activity = fields.Float(
        compute='_compute_activity_info', string='Amount Per Activity',
        multi='activity', store=True)

    # Compute Section
    def _compute_timesheet_group_id(self):
        pass

    def _set_timesheet_group_id(self):
        pass

    @api.one
    @api.depends('activity_ids')
    def _compute_activity_info(self):
        self.activity_qty = len(self.activity_ids)
        self.amount_per_activity = self.amount / len(self.activity_ids)

    # Views section
    @api.one
    @api.onchange('timesheet_group_id')
    def on_change_timesheet_group_id(self):
        if self.timesheet_group_id:
            self.activity_ids = self.timesheet_group_id.activity_ids.ids
        else:
            self.activity_ids = False
