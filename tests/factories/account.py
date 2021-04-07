# -*- coding: utf-8 -*-

import datetime

import factory
import factory_trytond

from .company import Company
from .party import Party
from .sequence import Sequence


class AccountTemplateType(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.account.type.template'

    name = factory.Faker('word')
    statement = 'balance'


class AccountTemplate(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.account.template'

    code = factory.Sequence(lambda n: str(n))
    name = factory.Faker('word')
    type = factory.SubFactory(AccountTemplateType)


class AccountType(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.account.type'

    company = factory.SubFactory(Company)
    name = factory.Faker('word')
    template = factory.SubFactory(AccountTemplateType)
    statement = 'balance'


class Account(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.account'

    name = factory.Faker('word')
    code = factory.SelfAttribute('template.code')
    template = factory.SubFactory(AccountTemplate)
    type = factory.SubFactory(
        AccountType,
        company=factory.SelfAttribute('..company'),
    )


class AccountJournal(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.journal'

    name = factory.Faker('word')
    type = 'cash'
    sequence = factory.SubFactory(
        Sequence,
        code='account.journal',
    )


class AccountBankStatementJournal(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.bank.statement.journal'

    company = factory.SubFactory(Company)
    name = factory.Faker('word')
    currency = factory.SelfAttribute('company.currency')
    journal = factory.SubFactory(AccountJournal)
    account = factory.SubFactory(Account)


class AccountBankStatement(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.bank.statement'

    company = factory.SubFactory(Company)
    journal = factory.SubFactory(AccountBankStatementJournal)
    date = factory.LazyAttribute(lambda o: datetime.datetime.now())


class AccountBankStatementLine(factory_trytond.TrytonFactory):
    class Meta:
        model = 'account.bank.statement.line'

    statement = factory.SubFactory(
        AccountBankStatementJournal,
        company=factory.SelfAttribute('..company'),
    )
    company = factory.SubFactory(Company)
    date = factory.LazyAttribute(lambda o: datetime.datetime.now())
    description = factory.Faker('word')
    amount = factory.Faker(
        'pydecimal', min_value=1, max_value=100, right_digits=2)
    party = factory.SubFactory(Party)


class AnalyticAccount(factory_trytond.TrytonFactory):
    class Meta:
        model = 'analytic_account.account'

    name = factory.Faker('word')
    code = factory.Faker('word')
    company = factory.SubFactory(Company)
    state = 'opened'


class AnalyticRootAccount(AnalyticAccount):

    type = 'root'
    parent = None


class NormalAnalyticAccount(factory_trytond.TrytonFactory):
    class Meta:
        model = 'analytic_account.account'

    name = factory.Faker('word')
    code = factory.Faker('word')
    company = factory.SubFactory(Company)
    type = 'normal'
    parent = factory.SubFactory(AnalyticRootAccount)
    root = factory.SubFactory(
        AnalyticRootAccount,
        company=factory.SelfAttribute('..company'),
    )
    state = 'opened'


class AnalyticAccountEntry(factory_trytond.TrytonFactory):
    class Meta:
        model = 'analytic.account.entry'

    class Params:
        company = factory.SubFactory(Company)

    root = factory.SubFactory(
        AnalyticRootAccount,
        company=factory.SelfAttribute('..company'),
    )
    account = factory.SubFactory(
        NormalAnalyticAccount,
        root=factory.SelfAttribute('..root'),
        company=factory.SelfAttribute('..company'),
    )
