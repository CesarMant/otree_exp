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

author = 'César Mantilla'

doc = """
Trust game with information to the truster/trustee about other's ethnicity or religion.
"""

class Constants(BaseConstants):

    name_in_url = 'trustfield'
    players_per_group = 2
    num_rounds = 5

    endowment = c(10)
    mult_factor = 3
    showupfee = 40
    question_trustA_correct = c(14)
    question_trustB_correct = c(8)


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round
            for p in self.get_players():
                p.participant.vars['ethnic'] = random.choice(['Dai','Han'])
                p.participant.vars['religion'] = random.choice(['Buddhist','Christian'])


class Group(BaseGroup):

    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, 1),
        doc="""Amount sent by P1""",
        )
    
    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        )

    def set_payoffs_s1(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.prepayoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.prepayoff = self.sent_amount * Constants.mult_factor - self.sent_back_amount

    def set_payoffs_final(self):
        paying_round = self.session.vars['paying_round']
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = p1.prepayoff
        p2.payoff = p2.prepayoff

class Player(BasePlayer):
    
    ethnic_in = models.CharField(initial=None,
                              choices=['Dai','Han'],
                              widget=widgets.RadioSelect())
    religion_in = models.CharField(initial=None,
                              choices=['Buddhist','Christian','None (atheist)'],
                              widget=widgets.RadioSelect())
    def other_eth(self):
        return self.get_others_in_group()[0].participant.vars['ethnic']
    def other_relig(self):
        return self.get_others_in_group()[0].participant.vars['religion']

    prepayoff = models.CurrencyField()

    question_trustA = models.CurrencyField()
    question_trustB = models.CurrencyField()

