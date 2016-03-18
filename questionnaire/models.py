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
Questionnaire to apply after the experiment
"""


class Constants(BaseConstants):
    name_in_url = 'questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    identification1 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons of your same ethnicity living in Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())

    identification2 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons of your same ethnicity living outside Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())

    identification3 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons with your same confession living in Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())

    identification4 = models.PositiveIntegerField(initial=None,
                            choices=range(1, 8),
                            verbose_name='Persons with your same confession living outside Xishuangbanna',
                            widget=widgets.RadioSelectHorizontal())