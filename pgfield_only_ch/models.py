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
This is a public goods game with second-party punishment
to be implemented in the field. In Chinese.
"""

class Constants(BaseConstants):
    name_in_url = 'pgfield_only_ch'
    players_per_group = 4
    num_rounds = 2
    question_pg1_correct = c(14)
    question_pg2_correct = c(10)

    endowment = c(10)
    showupfee = c(40)
    effic_factor = 1.6 # Efficiency factor for the public goods game
    punish_tech = 3    # Efficiency of the punishment technology: 1 spent point reduces the payoff 3 points

    # Variables to call ethnicity and religion
    ethnicity_dai = u'傣'            #'Dai'
    ethnicity_han = u'汉'            #'Han'
    religion_buddhist = u'佛教'      #'Buddhist'
    religion_christian = u'基督教'   #'Christian'
    religion_none = u'无宗教信仰'    #'None (atheist)'

    # Change this parameter according to the session size
    total_groups = 3 # Assuming 12 subjects to test
    # total_groups = 5 # In the sessions with 20 subject this must be uncommented


class Subsession(BaseSubsession):
    pass
    # This part must be left as comment when the full_game app is running
    # Uncomment only to run the pgfield app
    def before_session_starts(self):
        if self.round_number == 1:
            for p in self.get_players():
                p.participant.vars['ethnic'] = random.choice([u'傣',u'汉']) #(['Dai','Han'])
                p.participant.vars['religion'] = random.choice([u'佛教',u'基督教']) #(['Buddhist','Christian'])

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
    total_punish_p1 = models.CurrencyField()
    total_punish_p2 = models.CurrencyField()
    total_punish_p3 = models.CurrencyField()
    total_punish_p4 = models.CurrencyField()

    # Function to compute the payoffs after the contribution to the public goods game
    def set_payoffs_s1(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.effic_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff_s1 = Constants.endowment - p.contribution + self.individual_share

    # Function to compute the payoffs after the punishment stage
    def set_payoffs_s2(self):
        # Compute the total punishment points received by each player
        self.total_punish_p1 = sum([p.punish_p1 for p in self.get_players()])
        self.total_punish_p2 = sum([p.punish_p2 for p in self.get_players()])
        self.total_punish_p3 = sum([p.punish_p3 for p in self.get_players()])
        self.total_punish_p4 = sum([p.punish_p4 for p in self.get_players()])

        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)
        p4 = self.get_player_by_id(4)

        # Update the payoff after deducting allocated and received punishment points
        # Payments of each round are stored as "prepayoff"
        p1.prepayoff = p1.payoff_s1 - self.total_punish_p1 * Constants.punish_tech - (p1.punish_p2 + p1.punish_p3 + p1.punish_p4)
        p2.prepayoff = p2.payoff_s1 - self.total_punish_p2 * Constants.punish_tech - (p2.punish_p1 + p2.punish_p3 + p2.punish_p4)
        p3.prepayoff = p3.payoff_s1 - self.total_punish_p3 * Constants.punish_tech - (p3.punish_p1 + p3.punish_p2 + p3.punish_p4)
        p4.prepayoff = p4.payoff_s1 - self.total_punish_p4 * Constants.punish_tech - (p4.punish_p1 + p4.punish_p2 + p4.punish_p3)

class Player(BasePlayer):
    contribution = models.CurrencyField(choices=currency_range(0, Constants.endowment, 1),)

    # payoff_s1 is the payment each round before the punishment stage
    payoff_s1 = models.CurrencyField()
    # prepayoff is the payment each round after the punishment stage
    prepayoff = models.CurrencyField()
    # payoff_block2 is the cumulative payoff of all the rounds in the public goods game
    payoff_block2 = models.CurrencyField()

    # Allocation of punishment points to each subject
    punish_p1 = models.CurrencyField(min=0, max=Constants.endowment, null = True)
    punish_p2 = models.CurrencyField(min=0, max=Constants.endowment, null = True)
    punish_p3 = models.CurrencyField(min=0, max=Constants.endowment, null = True)
    punish_p4 = models.CurrencyField(min=0, max=Constants.endowment, null = True)

    # Variables to store the responses to the understanding questions
    question_pg1 = models.CurrencyField()
    question_pg2 = models.CurrencyField()

    ethnicity = models.CharField()
    religion = models.CharField()

    def get_ethnicity(self):
        return self.in_all_rounds()[0].participant.vars['ethnic']

    def get_religion(self):
        return self.in_all_rounds()[0].participant.vars['religion']
