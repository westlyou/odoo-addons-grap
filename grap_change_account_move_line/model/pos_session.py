# -*- encoding: utf-8 -*-
##############################################################################
#
#    GRAP - Change Account Move Lines Module for Odoo
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
# flake8: noqa

from openerp.osv import osv, fields
from openerp.osv.orm import Model
from openerp.tools.translate import _
from openerp import netsvc

class pos_session(Model):
    _inherit = 'pos.session'

    # OverWrite section
    def _confirm_orders(self, cr, uid, ids, context=None):
        """Generate Sale Entries"""
        wf_service = netsvc.LocalService("workflow")
        ap_obj = self.pool['account.period']
        po_obj = self.pool['pos.order']
        aj_obj = self.pool['account.journal']
        am_obj = self.pool['account.move']

        self._remove_draft_orders(cr, uid, ids, context=context)

        for ps in self.browse(cr, uid, ids, context=context):
            #parse the lines to group the ids according to the key fields
            groups = {}
            for po in ps.order_ids:
                if po.state not in ('paid', 'invoiced'):
                    raise osv.except_osv(
                        _('Error!'),
                        _("You cannot confirm all orders of this session,"
                        " because they have not the 'paid' status %s" % (
                        po.name)))
                if po.state == 'paid':
                    keys = (po.session_id.stop_at[:10])
                    groups.setdefault(keys,[])
                    groups[keys].append(po.id)

            # Create an Account move for each Key
            for key in groups.keys():
                (date) = key
                po_ids = groups[key]
                aj_id = ps.config_id.journal_id.id
                am_vals = {
                    'ref' : ps.name, 
                    'journal_id' : aj_id, 
                    'date': date,
                    }

                # if the journal is set to check the date is in the period,
                # find the period corresponding to the date
                if aj_obj.browse(cr, uid, aj_id, context=context).allow_date:
                    ap_id = ap_obj.find(cr, uid, dt=date, context=context)[0]
                    am_vals['period_id'] = ap_id

                am_id = am_obj.create(
                    cr, uid, am_vals, context=context)
                po_obj._create_account_move_line(
                    cr, uid, po_ids, ps, am_id, context=context)
                for po_id in po_ids:
                    # finish the workflow with an empty step
                    wf_service.trg_validate(
                        uid, 'pos.order', po_id, 'done', cr)
        return True


    def wkf_action_close(self, cr, uid, ids, context=None):
        bsl = self.pool.get('account.bank.statement.line')
        for record in self.browse(cr, uid, ids, context=context):
            for st in record.statement_ids:
                if st.difference and st.journal_id.cash_control == True:
                    if st.difference > 0.0:
                        name= _('Point of Sale Profit')
                        account_id = st.journal_id.profit_account_id.id
                    else:
                        account_id = st.journal_id.loss_account_id.id
                        name= _('Point of Sale Loss')
                    if not account_id:
                        raise osv.except_osv( _('Error!'),
                        _("Please set your profit and loss accounts on your payment method '%s'. This will allow OpenERP to post the difference of %.2f in your ending balance. To close this session, you can update the 'Closing Cash Control' to avoid any difference.") % (st.journal_id.name,st.difference))
                    bsl.create(cr, uid, {
                        'statement_id': st.id,
                        'amount': st.difference, 
                        'ref': record.name,
                        'name': name,
                        'account_id': account_id
                    }, context=context)

                if st.journal_id.type == 'bank':
                    st.write({'balance_end_real' : st.balance_end})
                if st.journal_id.type != 'sale':
                    self.button_confirm_pos(cr, uid, [st.id], record.name, context=context)
        return super(pos_session, self).wkf_action_close(cr, uid, ids, context=context)


    ### Private section

    def button_confirm_pos(self, cr, uid, ids, session_name, context=None):
        """Generate Bank Entries"""
        is_obj = self.pool['ir.sequence']
        st_obj = self.pool['account.bank.statement']
        context = context or {}

        for st in st_obj.browse(cr, uid, ids, context=context):
            j_type = st.journal_id.type
            company_currency_id = st.journal_id.company_id.currency_id.id

            # Preliminary checks
            if not st_obj.check_status_condition(cr, uid, st.state, journal_type=j_type):
                continue

            st_obj.balance_check(cr, uid, st.id, journal_type=j_type, context=context)
            if (not st.journal_id.default_credit_account_id) \
                    or (not st.journal_id.default_debit_account_id):
                raise osv.except_osv(_('Configuration Error!'),
                        _('Please verify that an account is defined in the journal.'))

            if not st.name == '/':
                st_number = st.name
            else:
                c = {'fiscalyear_id': st.period_id.fiscalyear_id.id}
                if st.journal_id.sequence_id:
                    st_number = is_obj.next_by_id(cr, uid, st.journal_id.sequence_id.id, context=c)
                else:
                    st_number = is_obj.next_by_code(cr, uid, 'account.bank.statement', context=c)

            for line in st.move_line_ids:
                if line.state <> 'valid':
                    raise osv.except_osv(_('Error!'),
                            _('The account entries lines are not in valid state.'))
            for st_line in st.line_ids:
                if st_line.analytic_account_id:
                    if not st.journal_id.analytic_journal_id:
                        raise osv.except_osv(_('No Analytic Journal!'),_("You have to assign an analytic journal on the '%s' journal!") % (st.journal_id.name,))
                if not st_line.amount:
                    continue

            #parse the lines to group the ids according to the key fields
            groups = {}
            for line in st.line_ids:
                if line.pos_statement_id\
                        and line.pos_statement_id.state == 'invoiced':
                    partner_id = line.partner_id.id
                else:
                    partner_id = False
                keys = (
                    line.account_id.id, 
                    partner_id,
                    line.journal_id.id, 
                    st.period_id.id, 
                    st_line.statement_id.pos_session_id.stop_at[:10], 
                    st_line.analytic_account_id, 
                    st_line.amount>0)
                groups.setdefault(keys,[])
                groups[keys].append(line.id)

            #for each group, create account_move and account_move_lines
            i = 0
            for key in groups.keys():
                i +=1
                move_number = st_number + "/" + str(i)
                line_ids = groups[key]
                move_id = self.create_move_from_st_lines(cr, uid, line_ids, st, move_number, session_name, key, context)

            st_obj.write(cr, uid, [st.id], {
                    'name': st_number,
                    'balance_end_real': st.balance_end
            }, context=context)
            st_obj.message_post(cr, uid, [st.id], body=_('Statement %s confirmed, journal items were created.') % (st_number,), context=context)
        if context.get('period_id',False): del context['period_id']
        if context.get('journal_id',False): del context['journal_id']
        return st_obj.write(cr, uid, ids, {'state':'confirm'}, context=context)


    def create_move_from_st_lines(self, cr, uid, ids, st, st_number, session_name, key, context=None):
        """Create the account move and lines from the statement lines.

           :param int/long st_id: ID of the account.bank.statement to create the move from.
           :param int/long company_currency_id: ID of the res.currency of the company
           :param char st_number: will be used as the name of the generated account move
           :return: ID of the account.move created
        """

        if context is None:
            context = {}

        (account_id, partner_id, journal_id, period_id, date, analytic_account_id, debit) = key
        am_obj = self.pool['account.move']
        aml_obj = self.pool['account.move.line']

#        if the journal is set to check the date is in the period, find the period corresponding to the date
        if self.pool.get('account.journal').browse(cr, uid, journal_id, context=context).allow_date:
            period_id = self.pool.get('account.period').find(cr, uid, dt=date, context=context)[0]

        move_vals = {
            'journal_id': journal_id,
            'partner_id': partner_id,
            'period_id': period_id,
            'date': date,
            'name': st_number,
            'ref': session_name,
            }
        move_id = am_obj.create(cr, uid, move_vals, context=context)
        bank_move_vals = self._prepare_bank_move_lines_pos(cr, uid, st, move_id, ids, st_number, key, context=context)
        move_line_id = aml_obj.create(cr, uid, bank_move_vals, context=context)

        counterpart_move_vals = self._prepare_counterpart_move_lines_pos(cr, uid, st, move_id, ids, st_number, key, context=context)
        aml_obj.create(cr, uid, counterpart_move_vals, context=context)

        # Bank statements will not consider boolean on journal entry_posted
        am_obj.post(cr, uid, [move_id], context=context)
        return move_id

    def _prepare_bank_move_lines_pos(self, cr, uid, st, move_id, ids, st_number, key, context=None):
        """Compute the args to build the dict of values to create the bank move line from a
           statement by calling the _prepare_move_line_vals. This method may be
           overridden to implement custom move generation (making sure to call super() to
           establish a clean extension chain).

           :param browse_record st_line: account.bank.statement.line record to
                  create the move from.
           :param int/long move_id: ID of the account.move to link the move line
           :param float amount: amount of the move line
           :param int/long company_currency_id: ID of currency of the concerned company
           :return: dict of value to create() the bank account.move.line
        """
        (account_id, partner_id, journal_id, period_id, date, anl_id, debit) = key
        amount = 0
        for st_line in self.pool.get('account.bank.statement.line').browse(cr, uid, ids, context=context):
            amount += st_line.amount

        debit = ((amount<0) and -amount) or 0.0
        credit =  ((amount>0) and amount) or 0.0

        return {
            'name': st.name,
            'date': st.date,
            'move_id': move_id,
            'account_id': account_id,
            'partner_id': partner_id,
            'credit': credit,
            'debit': debit,
            'statement_id': st.id,
            'journal_id': journal_id,
            'period_id': period_id,
            'analytic_account_id': anl_id,
        }

    def _prepare_counterpart_move_lines_pos(self, cr, uid, st, move_id, ids, st_number, key, context=None):
        """Compute the args to build the dict of values to create the counter part move line from a
           statement by calling the _prepare_move_line_vals. This method may be
           overridden to implement custom move generation (making sure to call super() to
           establish a clean extension chain).

           :param browse_record st_line: account.bank.statement.line record to
                  create the move from.
           :param int/long move_id: ID of the account.move to link the move line
           :param float amount: amount of the move line
           :param int/long account_id: ID of account to use as counter part
           :param int/long company_currency_id: ID of currency of the concerned company
           :return: dict of value to create() the bank account.move.line
        """
        (account_id, partner_id, journal_id, period_id, date, anl_id, debit) = key
        amount = 0
        for st_line in self.pool.get('account.bank.statement.line').browse(cr, uid, ids, context=context):
            amount += st_line.amount

        acc_id = ((amount<=0) and st.journal_id.default_debit_account_id.id) or st.journal_id.default_credit_account_id.id
        debit = ((amount > 0) and amount) or 0.0
        credit =  ((amount < 0) and -amount) or 0.0

        return {
            'name': st.name,
            'date': st.date,
            'move_id': move_id,
            'account_id': acc_id,
            'partner_id': partner_id,
            'credit': credit,
            'debit': debit,
            'statement_id': st.id,
            'journal_id': journal_id,
            'period_id': period_id,
            'analytic_account_id': anl_id,
        }
