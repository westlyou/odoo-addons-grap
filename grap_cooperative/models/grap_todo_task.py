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


class GrapTodoTask(models.Model):
    _name = 'grap.todo.task'
    _order = 'state desc, name'

    # Constant Section
    _GRAP_TODO_TASK_STATE = [
        ('1_draft', 'Draft'),
        ('2_qualified', 'Qualified'),
        ('3_in_progress', 'In Progress'),
        ('4_waiting_migration', 'Waiting Migration'),
        ('5_done', 'In Production'),
        ('6_canceled', 'Canceled'),
    ]

    _GRAP_TODO_TASK_IMPORTANCE = [
        ('undefined', 'Undefined'),
        ('low', 'Low'),
        ('average', 'Average'),
        ('high', 'High'),
    ]

    # Field Function Section
    @api.one
    @api.depends('total_days', 'made_days')
    def _compute_left_days(self):
        self.left_days = self.total_days - self.made_days

    # Columns section
    name = fields.Char(string='Name', required=True)

    total_days = fields.Float(
        string='Total Days', digits=(9, 1), required=True, default=0)

    made_days = fields.Float(
        string='Made Days', digits=(9, 1), required=True, default=0)

    left_days = fields.Float(
        compute='_compute_left_days', string='Left Days', store=True)

    start_date = fields.Date(
        string='Start Date', required=True, default=fields.Date.context_today)

    stop_date = fields.Date(string='Stop date')

    note = fields.Text(string='Description')

    internal_note = fields.Text(string='Internal Note')

    state = fields.Selection(
        selection=_GRAP_TODO_TASK_STATE, string='State', required=True,
        default='1_draft')

    importance = fields.Selection(
        selection=_GRAP_TODO_TASK_IMPORTANCE, string='Importance',
        required=True, default='undefined')

    applicant_ids = fields.Many2many(
        comodel_name='grap.member', relation='grap_todo_task_member_rel',
        column1='todo_task_id', column2='member_id', string='Applicants')

    worker_ids = fields.Many2many(
        comodel_name='grap.people', relation='grap_todo_task_people_rel',
        column1='todo_task_id', column2='people_id', string='Workers')

    # State section
    @api.one
    def state_previous(self):
        for index in range(len(self._GRAP_TODO_TASK_STATE) - 1):
            if self.state == self._GRAP_TODO_TASK_STATE[index + 1][0]:
                self.state = self._GRAP_TODO_TASK_STATE[index][0]

    @api.one
    def state_next(self):
        for index in range(len(self._GRAP_TODO_TASK_STATE) - 1):
            if self.state == self._GRAP_TODO_TASK_STATE[index][0]:
                self.state = self._GRAP_TODO_TASK_STATE[index + 1][0]
