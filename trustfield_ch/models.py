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
about other's ethnicity or religion. In Chinese.
"""

class Constants(BaseConstants):
    name_in_url = 'trustfield_ch'
    players_per_group = 2
    num_rounds = 5

    ### Change this parameter according to the session size ###
    ### Comment / Uncomment the right one ###
    num_senders_per_type = 3 ## Assuming 12 subjects
    #num_senders_per_type = 4 ## Assuming 16 subjects
    #num_senders_per_type = 5 ## Assuming 20 subjects

    # Game parameters
    endowment = c(50)
    showupfee = c(40)
    mult_factor = 3 # Efficiency factor in the transfer on the trust game

    # Variables to display ethnicity and religion options
    ethnicity_dai = u'傣'            #'Dai'
    ethnicity_han = u'汉'            #'Han'
    religion_buddhist = u'佛教'      #'Buddhist'
    religion_christian = u'基督教'   #'Christian'
    religion_none = u'无宗教信仰'    #'None (atheist)'

    # Responses to the understanding questions
    question_trustA_correct = c(70)
    question_trustB_correct = c(40)


class Subsession(BaseSubsession):
    def before_session_starts(self):  # Select the payment round from the beginning
        if self.round_number == 1:
            paying_round = random.randint(1, Constants.num_rounds)
            self.session.vars['paying_round'] = paying_round  # Store the payment round

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

    def set_payoffs_s1(self): # Compute payoffs for both players in the trust game
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
                                 # choices=[u'傣',u'汉'], # choices=['Dai','Han']
                                 widget=widgets.RadioSelect())
    # Input variable to ask the participants' religion
    religion_in = models.CharField(initial=None,
                                   choices=[Constants.religion_buddhist,
                                            Constants.religion_christian,
                                            Constants.religion_none],
                                   # choices=[u'佛教',u'基督教',u'无宗教信仰'], #choices=['Buddhist','Christian','None (atheist)'],
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
                              verbose_name='I agree to participate: ',
                              widget=widgets.RadioSelectHorizontal())
