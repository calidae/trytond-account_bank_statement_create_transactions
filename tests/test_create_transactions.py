
from datetime import date, datetime
from decimal import Decimal
import unittest

from trytond.pool import Pool
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import with_transaction
from trytond.transaction import Transaction

from . import factories


class CreateTransactionsTestCase(ModuleTestCase):
    'Test Create Transactions module'
    module = 'create_transactions'

    @with_transaction(0)
    def test_create_transactions(self):

        pool = Pool()
        StatementLine = pool.get('account.bank.statement.line')
        StatementMoveLine = Pool().get('account.bank.statement.move.line')
        CreateTransactions = pool.get(
            'account.create_transactions',
            type='wizard'
        )

        # GIVEN
        company = factories.Company.create()
        analytic_accounts = factories.AnalyticAccountEntry.create_batch(2)
        journal_cash = factories.AccountJournal.create(type='cash')
        account_receivable = factories.Account.create(
            company=company,
            type__type='receivable',
            type__receivable=True,
            bank_reconcile=True,
            reconcile=True,
        )
        statement_journal = factories.AccountBankStatementJournal.create(
            company=company,
            journal=journal_cash,
            account=account_receivable,
        )
        statement = factories.AccountBankStatement.create(
            company=company,
            journal=statement_journal,
        )
        statement_line_1 = factories.AccountBankStatementLine.create(
            company=company,
            date=datetime(2020, 1, 1, 1, 1, 1),
            statement=statement,
            amount=Decimal('10.0'),
        )
        statement_line_2 = factories.AccountBankStatementLine.create(
            company=company,
            date=datetime(2020, 2, 2, 1, 1, 1),
            statement=statement,
            amount=Decimal('25.0'),
        )
        StatementLine.confirm([statement_line_1, statement_line_2])

        # WHEN
        with Transaction().set_context(
                active_ids=[statement_line_1.id, statement_line_2.id]
        ):
            (session_id, _, _) = CreateTransactions.create()
            wiz = CreateTransactions(session_id)
            default_start = wiz.default_start([])
            self.assertEqual(
                default_start['lines'],
                [statement_line_1.id, statement_line_2.id],
            )
            wiz.start.account = account_receivable
            wiz.start.analytic_accounts = analytic_accounts
            wiz.start.lines = [statement_line_1, statement_line_2]
            wiz.start.description = 'H3110'
            wiz.transition_generate()

        # THEN
        move_lines = StatementMoveLine.search([])

        line_1 = next(
            (
                move_line for move_line in move_lines
                if move_line.line == statement_line_1
            )
        )
        line_2 = next(
            (
                move_line for move_line in move_lines
                if move_line.line == statement_line_2
            )
        )

        self.assertEqual(line_1.account, account_receivable)
        self.assertEqual(line_1.amount, 10)
        self.assertEqual(line_1.date, date(2020, 1, 1))
        self.assertEqual(line_1.description, 'H3110')
        self.assertCountEqual(
            [line.account for line in line_1.analytic_accounts],
            [line.account for line in analytic_accounts],
        )
        self.assertCountEqual(
            [line.root for line in line_1.analytic_accounts],
            [line.root for line in analytic_accounts],
        )

        self.assertEqual(line_2.account, account_receivable)
        self.assertEqual(line_2.amount, 25)
        self.assertEqual(line_2.date, date(2020, 2, 2))
        self.assertEqual(line_2.description, 'H3110')
        self.assertCountEqual(
            [line.account for line in line_2.analytic_accounts],
            [line.account for line in analytic_accounts],
        )
        self.assertCountEqual(
            [line.root for line in line_2.analytic_accounts],
            [line.root for line in analytic_accounts],
        )


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(
        unittest.TestLoader().loadTestsFromTestCase(
            CreateTransactionsTestCase
        )
    )
    return suite
