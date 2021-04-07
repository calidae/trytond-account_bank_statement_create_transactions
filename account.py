
from logging import getLogger

from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.transaction import Transaction
from trytond.pool import Pool
from trytond.model import ModelView
from trytond.model import fields
from trytond.wizard import Wizard
from trytond.wizard import StateView
from trytond.wizard import Button
from trytond.wizard import StateTransition


__all__ = [
    'CreateTransactionsStart',
    'CreateTransactions',
]

_logger = getLogger(__name__)


class CreateTransactionsStart(ModelView):
    'Create transactions from bank statement lines Start View'
    __name__ = 'account.create_transactions.start'

    lines = fields.One2Many(
        'account.bank.statement.line',
        None,
        'Selected Bank Statement Lines',
        readonly=True,
    )

    account = fields.Many2One(
        'account.account',
        'Account',
        required=True,
        domain=[
            ('kind', '!=', 'view'),
        ],
    )
    analytic_accounts = fields.One2Many(
        'analytic.account.entry',
        None,
        'Analytic Accounts',
    )
    description = fields.Text('Description')


class CreateTransactions(Wizard):
    'Create transactions from bank statement lines'
    __name__ = 'account.create_transactions'

    start = StateView(
        'account.create_transactions.start',
        'create_transactions.create_transactions_start_view_form',
        [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button(
                'Generate',
                'generate',
                'tryton-ok',
                True
            ),
        ]
    )

    generate = StateTransition()

    def default_start(self, args):
        active_ids = Transaction().context['active_ids']
        self.check_selection(active_ids)

        return {'lines': active_ids}

    def check_selection(self, active_ids):
        StatementLine = Pool().get('account.bank.statement.line')

        if not active_ids:
            raise UserError(gettext('create_transactions.no_active_ids'))

        lines = StatementLine.browse(active_ids)
        if any([line.state != 'confirmed' for line in lines]):
            raise UserError(gettext('create_transactions.invalid_state'))
        if any([line.reconciled for line in lines]):
            raise UserError(
                gettext('create_transactions.must_not_be_reconciled')
            )

    def transition_generate(self):
        StatementMoveLine = Pool().get('account.bank.statement.move.line')
        if self.start.lines:
            analytic_accounts = [
                {
                    'account': acc.account,
                    'root': acc.root,
                }
                for acc in self.start.analytic_accounts
            ]

            StatementMoveLine.create([
                {
                    'line': line.id,
                    'date': line.date.date(),
                    'amount': line.amount,
                    'account': self.start.account,
                    'analytic_accounts':  [
                        ('create', analytic_accounts),
                    ] if analytic_accounts else [],
                    'description': self.start.description,
                }
                for line in self.start.lines
            ])
        return 'end'
