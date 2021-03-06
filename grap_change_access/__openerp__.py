# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Access module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Julien WESTE
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
{
    'name': 'GRAP - Change access for GRAP users',
    'version': '1.0',
    'category': 'GRAP - Custom',
    'description': """
Remove update / delete access for basic users for some model
============================================================

Features :
----------
    * 'product_category' is readonly;
    * 'product_uom' is readonly;
    * 'product_uom_categ' is readonly;
    * 'res_country' is readonly;
    * 'res_country_state' is readonly;
    * 'email_template' is readonly;
    * 'account_period' is readonly (except for account_manager);
    * stock_location.complete_name is refactored;


Copyright, Author and Licence :
-------------------------------
    * Copyright : 2014, Groupement Régional Alimentaire de Proximité;
    * Authors:
        * Julien WESTE;
        * Sylvain LE GAL (https://twitter.com/legalsylvain);
    * Licence : AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'email_template',
        'delivery',
        'product',
        'stock',
        'point_of_sale',
        'base',
        'purchase',
        'sale',
        'procurement',
        'account_fiscal_company',
        'crm',
        'base_calendar',
    ],
    'data': [
        'security/res_groups.yml',
        'security/ir.model.access.csv',
    ],
}
