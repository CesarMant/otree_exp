# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class questions_1(Page):
    form_model = models.Player
    form_fields = ['identification1',
                   'identification2',
                   'identification3',
                   'identification4'
                   ]



page_sequence = [
    questions_1,
]
