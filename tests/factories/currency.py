# -*- coding: utf-8 -*-

from decimal import Decimal

import factory
import factory_trytond


class Currency(factory_trytond.TrytonFactory):
    class Meta:
        model = 'currency.currency'

    name = factory.Faker('currency_name')
    code = factory.Faker('currency_code')
    symbol = factory.Faker('currency_code')


class Euro(factory_trytond.TrytonFactory):
    class Meta:
        model = 'currency.currency'

    name = 'Euro'
    code = 'EUR'
    symbol = '€'
    digits = 2
    numeric_code = '978'
    rounding = Decimal('0.01')
