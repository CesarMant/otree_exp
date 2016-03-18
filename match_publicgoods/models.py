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
Matching protocol for the public goods game
"""

class Constants(BaseConstants):
    name_in_url = 'match_publicgoods'
    players_per_group = 4
    num_rounds = 2

    endowment = c(10)
    showupfee = c(40)
    effic_factor = 1.6 # Efficiency factor for the public goods game
    punish_tech = 3    # Efficiency of the punishment technology: 1 spent point reduces the payoff 3 points

    religion_buddhist = 'Buddhist'
    religion_christian = 'Christian'
    religion_none = 'None (atheist)'
    ethnicity_dai = 'Dai'
    ethnicity_han = 'Han'

    total_groups = 3


class Subsession(BaseSubsession):
    # This part must be left as comment when the full_game app is running
    # Uncomment only to run the pgfield app
    def before_session_starts(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['ethnic'] = random.choice(['Dai','Han'])
                p.participant.vars['religion'] = random.choice(['Buddhist','Christian'])

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
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    # Total punishment points allocated to each player are stored as a group level variable

    # Function to compute the payoffs after the contribution to the public goods game
    def set_payoffs_s1(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.effic_factor / Constants.players_per_group
        for p in self.get_players():
            p.prepayoff = Constants.endowment - p.contribution + self.individual_share


class Player(BasePlayer):
    contribution = models.CurrencyField(choices=currency_range(0, Constants.endowment, 1),)

    # prepayoff is the payment each round after the punishment stage
    prepayoff = models.CurrencyField()
    # payoff_block2 is the cumulative payoff of all the rounds in the public goods game
    payoff_block2 = models.CurrencyField()

    ethnicity = models.CharField()
    religion = models.CharField()

    def get_ethnicity(self):
        return self.in_all_rounds()[0].participant.vars['ethnic']

    def get_religion(self):
        return self.in_all_rounds()[0].participant.vars['religion']








