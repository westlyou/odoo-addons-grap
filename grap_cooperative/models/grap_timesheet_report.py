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

from openerp import tools, models, fields


class GrapTimesheetReport(models.Model):
    _name = 'grap.timesheet.report'
    _auto = False
    _table_name = 'grap_timesheet_report'

    # Column Section
    name = fields.Char(string='Name', readonly=True)

    amount = fields.Float(string='Amount', readonly=True)

    date = fields.Date(string='Date', readonly=True)

    week = fields.Char(string='Week', readonly=True)

    worker_id = fields.Many2one(
        comodel_name='grap.people', string='Worker', readonly=True)

    activity_id = fields.Many2one(
        comodel_name='grap.activity', string='Activity', readonly=True)

    type_id = fields.Many2one(
        comodel_name='grap.timesheet.type', string='Work Type', required=True)

    # Database View Section
    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table_name)
        cr.execute("""
CREATE OR REPLACE VIEW %s AS (
    SELECT
        row_number() OVER () as id,
        gt.date,
        gt.name,
        to_char(DATE_TRUNC('week',gt.date),'YYYY/MM/DD') as week,
        gt.type_id,
        gtar.activity_id,
        gt.worker_id,
        gt.amount_per_activity as amount
    FROM grap_timesheet_activity_rel gtar
    LEFT OUTER JOIN grap_timesheet gt
        ON gt.id = gtar.timesheet_id
)""" % (self._table_name))
