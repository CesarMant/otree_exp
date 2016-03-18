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
Matching protocol for the trust game
"""


class Constants(BaseConstants):
    name_in_url = 'match_trustgame'
    players_per_group = 2
    num_rounds = 2

    endowment = c(10)
    mult_factor = 3
    showupfee = c(40)
    religion_buddhist = 'Buddhist'
    religion_christian = 'Christian'
    religion_none = 'None (atheist)'
    ethnicity_dai = 'Dai'
    ethnicity_han = 'Han'
    num_senders_per_type = 2


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round # Store the payment round

    def get_ethnicity_dai(self):
        return [
            p for p in self.get_players() if p.get_ethnicity() == Constants.ethnicity_dai
        ]

    def get_ethnicity_han(self):
        return [
            p for p in self.get_players() if p.get_ethnicity() == Constants.ethnicity_han
        ]

    def get_religion_buddhist(self):
        return [
            p for p in self.get_players() if p.get_religion() == Constants.religion_buddhist
        ]

    def get_religion_christian(self):
        return [
            p for p in self.get_players() if p.get_religion() == Constants.religion_christian
        ]

    def get_religion_none(self):
        return [
            p for p in self.get_players() if p.get_religion() == Constants.religion_none
        ]


class Group(BaseGroup):
    # Amount sent in the trust game
    sent_amount = models.CurrencyField(
        choices=currency_range(0, Constants.endowment, 1),
        doc="""Amount sent by P1""",
        )
    # Amount sent back in the trust game
    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
    )

    def set_payoffs_s1(self): # Compute payoffs for both players in the trust game
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.payoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.payoff = self.sent_amount * Constants.mult_factor - self.sent_back_amount


class Player(BasePlayer):
    ethnic_in = models.CharField(initial=None,
                                 choices=[Constants.ethnicity_dai,
                                          Constants.ethnicity_han],
                                 widget=widgets.RadioSelect())
    # Input variable to ask the participants' religion
    religion_in = models.CharField(initial=None,
                                   choices=[Constants.religion_buddhist,
                                            Constants.religion_christian,
                                            Constants.religion_none],
                                   widget=widgets.RadioSelect())
    # Function defined to get the ethnicity of the other participant in the group in the trust game
    def other_eth(self):
        return self.get_others_in_group()[0].participant.vars['ethnic']

    # Function defined to get the religion of the other participant in the group in the trust game
    def other_relig(self):
        return self.get_others_in_group()[0].participant.vars['religion']

    def get_ethnicity(self):
        return self.in_all_rounds()[0].participant.vars['ethnic']

    def get_religion(self):
        return self.in_all_rounds()[0].participant.vars['religion']

    payoff_block1 = models.CurrencyField()
