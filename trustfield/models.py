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
Trust game with information to the truster/trustee
about other's ethnicity or religion. English version.
"""

class Constants(BaseConstants):
    name_in_url = 'trustfield'
    players_per_group = 2
    num_rounds = 5

    ### Change this parameter according to the session size ###
    ### Comment / Uncomment the right one ###
    num_senders_per_type = 3  ## Assuming 12 subjects
    #num_senders_per_type = 4  ## Assuming 16 subjects
    #num_senders_per_type = 5  ## Assuming 20 subjects

    # Game parameters
    endowment = c(50)
    showupfee = c(50)
    mult_factor = 3  # Efficiency factor in the transfer on the trust game

    # Variables to display ethnicity and religion options
    ethnicity_dai = 'Dai'
    ethnicity_han = 'Han'
    religion_buddhist = 'Buddhist'
    religion_christian = 'Christian'
    religion_none = 'None (atheist)'

    # Responses to the understanding questions
    question_trustA_correct = c(70)
    question_trustB_correct = c(40)


class Subsession(BaseSubsession):
    def before_session_starts(self):  # Select the payment round from the beginning
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round  # Store the payment round

            # Randomization of matching type per round (order effects):
            # When a=0 in round 2 and 3 the matching is with those of the same Ethnicity/Religion
            # When a=2 in round 2 and 3 the matching is with those of the other Ethnicity/Religion
            alter_round = random.choice([0, 2])
            self.session.vars['alter_round'] = alter_round

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
        choices=currency_range(0, Constants.endowment, 5),
        doc="""Amount sent by P1""",
        )
    # Amount sent back in the trust game
    sent_back_amount = models.CurrencyField(
        doc="""Amount sent back by P2""",
        )

    def set_payoffs_s1(self):  # Compute payoffs for both players in the trust game
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p1.prepayoff = Constants.endowment - self.sent_amount + self.sent_back_amount
        p2.prepayoff = self.sent_amount * Constants.mult_factor - self.sent_back_amount


class Player(BasePlayer):

    ethnic = models.CharField()     # Variable to store the participants' ethnicity
    religion = models.CharField()   # Variable to store the participants' religion
    # Input variable to ask the participants' ethnicity
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

    # Prepayoff is the payment of each round
    prepayoff = models.CurrencyField()
    # Payoff_block1 is the payment of the round selected to be paid
    # Block 1 refers to the trust game
    # Block 2 refers to the public goods game with punishment
    payoff_block1 = models.CurrencyField()

    # Variables to store the responses to the understanding questions
    question_trustA = models.CurrencyField()
    question_trustB = models.CurrencyField()

    # Variable to store the agreement to participate
    consent = models.CharField(initial=None,
                              choices=[('Yes', 'Yes'),
                                       ('No', 'No')],
                              widget=widgets.RadioSelectHorizontal())
