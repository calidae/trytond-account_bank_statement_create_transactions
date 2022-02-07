# -*- coding: utf-8 -*-

import factory
import factory_trytond


class Sequence(factory_trytond.TrytonFactory):
    class Meta:
        model = 'ir.sequence'

    name = factory.Faker('word')
    prefix = factory.Faker('pystr', max_chars=1)
    suffix = factory.Faker('pystr', max_chars=1)
