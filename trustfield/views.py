# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class Welcome(Page):
    def is_displayed(self):
        return self.subsession.round_number == 1
    
    form_model = models.Player
    form_fields = ['ethnic_in','religion_in']

    # Function defined to store the participant's ethnicity and religion in the dictionary
    # By storing the variable as self.player.participant.vars['name'] it can be accessed in other sessions
    def before_next_page(self):
        self.player.participant.vars['ethnic'] = self.player.ethnic_in
        self.player.participant.vars['religion'] = self.player.religion_in

    def vars_for_template(self):
        return {
            'exchange_rate': 0.4,
            }


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):

        # In the Send and SendBack pages the information shown in each round about the other player is different
        # Round 1: No information
        # Round 2: Ethnicity
        # Round 3: Religion
        # Round 4: Ethnicity
        # Round 5: Religion
        # The corresponding code is directly located in the Send.html and SendBack.html files

        dai_players = self.subsession.get_ethnicity_dai()  # Get list of Dai
        han_players = self.subsession.get_ethnicity_han()  # Get list of Han
        players = dai_players + han_players                # Combine the two lists
        # Define the list of senders: fixed in every shuffling
        # First 25% in the players list (Dai) + Last 25% in the players list (Han)
        senders = players[0:Constants.num_senders_per_type] + players[-Constants.num_senders_per_type:]

        if self.subsession.round_number == 1:
            ## 1. Random matching - only for receivers (senders are fixed)
            ## Create the same list of receivers as in Matching_same_ethnicity_1.
            ## Then shuffle it randomly
            receivers = players[Constants.num_senders_per_type:-Constants.num_senders_per_type]
            random.shuffle(receivers)   # Matching: random
        elif self.subsession.round_number == 2:
            ## 2. Matching_same_ethnicity_1 they are consecutive to pair Dai with Dai and Han with Han
            ## Define the list of receivers
            ## Second 25% in the players list (Dai) + Third 25% in the players list (Han)
            receivers = players[Constants.num_senders_per_type:-Constants.num_senders_per_type]
        elif self.subsession.round_number == 3:
            ## 3. Matching_same_ethnicity_2 they are consecutive to pair Dai with Dai and Han with Han
            ## Create the list of receivers in two steps: first the Dai and then the Han
            ## Reverse the order of both sublists of receivers to have another Dai-Dai / Han-Han matching
            group1_receivers = players[Constants.num_senders_per_type:2*Constants.num_senders_per_type]
            group1_receivers.reverse()
            group2_receivers = players[2*Constants.num_senders_per_type:-Constants.num_senders_per_type]
            group2_receivers.reverse()
            receivers = group1_receivers + group2_receivers
        elif self.subsession.round_number == 4:
            ## 4. Matching_other_ethnicity1
            ## Create the same list of receivers as in Matching_same_ethnicity_1.
            ## Then reverse it to have Dai-Han / Han-Dai matching
            receivers = players[Constants.num_senders_per_type:-Constants.num_senders_per_type]
            receivers.reverse()
        elif self.subsession.round_number == 5:
            ## 5. Matching_other_ethnicity2
            ## Create the same list of receivers as in Matching_same_ethnicity_2.
            ## Then reverse it to have Dai-Han / Han-Dai matching
            group1_receivers = players[Constants.num_senders_per_type:2*Constants.num_senders_per_type]
            group1_receivers.reverse()
            group2_receivers = players[2*Constants.num_senders_per_type:-Constants.num_senders_per_type]
            group2_receivers.reverse()
            receivers = group1_receivers + group2_receivers
            receivers.reverse()

        for group, sender, receiver in zip(self.subsession.get_groups(),
                                           senders,
                                           receivers):
            group.set_players([sender, receiver])


class WelcomeTrust(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Group
    
    def vars_for_template(self):
        return {
            'endowment_2': Constants.endowment * 0.5,
            'endowment_2x3': Constants.endowment * 1.5
            }


class Question_trust(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    # Fields to store the responses to understanding questions
    form_fields = ['question_trustA','question_trustB']


class Feedback_trust(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class Consent_form(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['consent']


class Send(Page):

    form_model = models.Group
    form_fields = ['sent_amount']

    def is_displayed(self):
        return self.player.id_in_group == 1


class WaitForP1(WaitPage):
    pass


class SendBack(Page):

    form_model = models.Group
    form_fields = ['sent_back_amount']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        return {
            'tripled_amount': self.group.sent_amount * Constants.mult_factor,
            'sent_A': Constants.endowment - self.group.sent_amount
            }

    def sent_back_amount_choices(self):
        return currency_range(
            c(0),
            self.group.sent_amount * Constants.mult_factor,
            c(5)
            )


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs_s1()
        if self.subsession.round_number == Constants.num_rounds:
            paid_round = self.session.vars['paying_round'] - 1
            for player in self.subsession.get_players():
                player_in_chosen_round = player.in_all_rounds()[paid_round]
                player.payoff_block1 = player_in_chosen_round.prepayoff
                player.participant.vars['payoff_block1'] = player.payoff_block1


class Results(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'player_in_all_rounds': self.player.in_all_rounds(),
            'paying_round': self.session.vars['paying_round'],
            'payoff_block1': self.player.payoff_block1
        }


page_sequence = [
    Welcome,
    # ShuffleWaitPage,
    WelcomeTrust,
    Question_trust,
    Feedback_trust,
    Consent_form,
    Send,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    Results
]
