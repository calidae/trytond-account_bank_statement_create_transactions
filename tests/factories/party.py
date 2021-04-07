# -*- coding: utf-8 -*-

import factory
import factory_trytond


class Party(factory_trytond.TrytonFactory):

    class Meta:
        model = 'party.party'

    name = factory.Faker('name')
