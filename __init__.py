
from trytond.pool import Pool
from . import account


def register():
    Pool.register(
        account.CreateTransactionsStart,
        module='create_transactions',
        type_='model',
    )
    Pool.register(
        account.CreateTransactions,
        module='create_transactions',
        type_='wizard',
    )
