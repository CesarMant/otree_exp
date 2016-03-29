# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class demographics(Page):
    form_model = models.Player
    form_fields = ['year_birth',
                   'month_birth',
                   'living_Xsh',
                   'year_Xsh',
                   'gender',
                   'ethnic_self',
                   'relig_self',
                   'marital_status',
                   'education',
                   'hh_register',
                   'current_register',
                   'other_register',
                   'health',
                   'satisfaction',
                   'employment',
                   # 'company',
    ]

class questions_1(Page):
    form_model = models.Player
    form_fields = ['identification1',
                   'identification2',
                   'identification3',
                   'identification4',
                   'belief_recipr1',
                   'belief_recipr2',
                   'positive_recipr1',
                   'positive_recipr2',
                   'positive_recipr3',
                   'negative_recipr1',
                   'negative_recipr2',
                   'negative_recipr3',
                   ]


class questions_2(Page):
    form_model = models.Player
    form_fields = ['trust1',
                   'trust2',
                   'trust3',
                   'trust4',
                   'trust5',
                   'pray',
                   'relig_activ',
                   'temple',
                   'donation',
                   'donated_amount',
                   'importance_relig',
                   'relig_father',
                   'relig_father_other',
                   'relig_mother',
                   'relig_mother_other',
                   'marriage_religion',
                   ]


class family(Page):
    form_model = models.Player
    form_fields = ['hh_income',
                   'income_contribute',
                   'self_contribute',
                   'self_contrib_amount',
                   'income_dependence',
                   'relative_wealth',
                   'ethnic_father',
                   'ethnic_father_other',
                   'ethnic_mother',
                   'ethnic_mother_other',
                   'marriage_ethnicity',
                   'ethnic_spouse',
                   'ethnic_spouse_other',
                   'relig_spouse',
                   'relig_spouse_other',
                   ]


page_sequence = [
    demographics,
    questions_1,
    questions_2,
    family,
]
