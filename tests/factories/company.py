# -*- coding: utf-8 -*-

import factory
import factory_trytond

from .currency import Euro
from .party import Party


class Company(factory_trytond.TrytonFactory):

    class Meta:
        model = 'company.company'

    class Params:
        euro = factory_trytond.ModelData('currency', 'eur')

    party = factory.SubFactory(Party)
    currency = factory.Maybe(
        'euro',
        factory.SelfAttribute('euro'),
        factory.SubFactory(Euro),
    )
