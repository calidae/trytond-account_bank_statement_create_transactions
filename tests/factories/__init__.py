# -*- coding: utf-8 -*-
import factory
factory.Faker._DEFAULT_LOCALE = 'es_ES'

from .account import * # NOQA: 401
from .company import * # NOQA: 401
from .currency import * # NOQA: 401
from .party import * # NOQA: 401
from .sequence import * # NOQA: 401
