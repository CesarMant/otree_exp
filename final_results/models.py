# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division

import random

import otree.models
from otree.db import models
from otree import widgets
from otree.common import Currency as c, currency_range, safe_json
from otree.constants import BaseConstants
from otree.models import BaseSubsession, BaseGroup, BasePlayer
# </standard imports>

author = 'Cesar Mantilla'

doc = """
Summary of game payments
"""


class Constants(BaseConstants):
    name_in_url = 'final_results'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    payoff_block1 = models.CurrencyField()
    payoff_block2 = models.CurrencyField()

    def set_final_payoff(self):
        self.payoff = self.payoff_block1 + self.payoff_block2