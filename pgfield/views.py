# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class WelcomePublicGoods(Page):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player

    def vars_for_template(self):
        return {
            'n_minus_one': Constants.players_per_group - 1,
            'endowment_2': Constants.endowment / 2,
            'contrib_others_high': Constants.endowment * (Constants.players_per_group - 1) * 0.7,
            'contrib_others_low': Constants.endowment * (Constants.players_per_group - 1)* 0.3,
            'contrib_total_high': Constants.endowment * (Constants.players_per_group - 1)* 0.7 + Constants.endowment / 2,
            'contrib_total_low': Constants.endowment * (Constants.players_per_group - 1)* 0.3 + Constants.endowment / 2,
            'payoff_ex_high': Constants.endowment * ((Constants.players_per_group - 1)* 0.7 + 0.5) * (Constants.effic_factor / Constants.players_per_group),
            'payoff_ex_low': Constants.endowment * ((Constants.players_per_group - 1)* 0.3 + 0.5) * (Constants.effic_factor / Constants.players_per_group),
            'payoff_high': Constants.endowment * 0.5 + Constants.endowment * ((Constants.players_per_group - 1)* 0.7 + 0.5) * (Constants.effic_factor / Constants.players_per_group),
            'payoff_low':  Constants.endowment * 0.5 + Constants.endowment * ((Constants.players_per_group - 1)* 0.3 + 0.5) * (Constants.effic_factor / Constants.players_per_group),
            }

class Question_pg(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['question_pg1','question_pg2']

class Feedback_pg(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1


class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def after_all_players_arrive(self):
        if self.subsession.round_number == 1:
            ppg = Constants.players_per_group
            mixed_groupsx2 = (Constants.total_groups-2)*2
            dai_players = self.subsession.get_ethnicity_dai() # Get list of Dai
            han_players = self.subsession.get_ethnicity_han() # Get list of Han
            pre_players = dai_players + han_players               # Combine the two lists
            pre_mixed_groups = pre_players[ppg:-ppg]
            mixed_groups = []
            for g in range(0, mixed_groupsx2, 1):
                mixed_groups.append(pre_mixed_groups[g])
                mixed_groups.append(pre_mixed_groups[g+mixed_groupsx2])
            players = pre_players[0:ppg] + pre_players[-ppg:] + mixed_groups
            group_matrix = []
            for i in range(0, len(players), ppg):
                group_matrix.append(players[i:i+ppg])
            self.subsession.set_groups(group_matrix)
        else:
            self.subsession.group_like_round(1)


# The ethnicity information of each player will be displayed twice:
# In the contribution stage and in the punishment stage
class Contribute(Page):

    form_model = models.Player
    form_fields = ['contribution']

    def vars_for_template(self):
        self.player.ethnicity = self.player.get_ethnicity()
        return{
            'ethnicity' : self.player.ethnicity
        }


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs_s1()


class Punishment1(Page):
    form_model = models.Player
    form_fields = ['punish_p2', 'punish_p3', 'punish_p4']

    def is_displayed(self):
        return self.player.id_in_group == 1

    def before_next_page(self):
        if self.player.punish_p1 is None:
            self.player.punish_p1 = 0


class Punishment2(Page):
    form_model = models.Player
    form_fields = ['punish_p1', 'punish_p3', 'punish_p4']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def before_next_page(self):
        if self.player.punish_p2 is None:
            self.player.punish_p2 = 0


class Punishment3(Page):
    form_model = models.Player
    form_fields = ['punish_p1', 'punish_p2', 'punish_p4']

    def is_displayed(self):
        return self.player.id_in_group == 3

    def before_next_page(self):
        if self.player.punish_p3 is None:
            self.player.punish_p3 = 0


class Punishment4(Page):
    form_model = models.Player
    form_fields = ['punish_p1', 'punish_p2', 'punish_p3']

    def is_displayed(self):
        return self.player.id_in_group == 4

    def before_next_page(self):
        if self.player.punish_p4 is None:
            self.player.punish_p4 = 0


class ResultsWaitPage2(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs_s2()


class Results(Page):

    def vars_for_template(self):
        for p in self.group.get_players(): # Function to compute total expenditure in punishing others
            p.punish_exp = p.punish_p1 + p.punish_p2 + p.punish_p3 + p.punish_p4
        return {
        'punish_exp': self.player.punish_exp,
        'eff_punish_p1' : Constants.punish_tech * self.group.total_punish_p1, # Values of total punishment for each player
        'eff_punish_p2' : Constants.punish_tech * self.group.total_punish_p2,
        'eff_punish_p3' : Constants.punish_tech * self.group.total_punish_p3,
        'eff_punish_p4' : Constants.punish_tech * self.group.total_punish_p4,
    }


class FinalResultsWaitPage(WaitPage):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        for player in self.subsession.get_players():
            player_in_all_rounds = player.in_all_rounds()
            player.payoff_block2 = sum([p.prepayoff for p in player_in_all_rounds])
            player.participant.vars['payoff_block2'] = player.payoff_block2


class FinalResults(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):

        return {
            'payoff_block2': self.player.payoff_block2
        }


page_sequence = [
    WelcomePublicGoods,
    Question_pg,
    Feedback_pg,
    ShuffleWaitPage,
    Contribute,
    ResultsWaitPage,
    Punishment1,
    Punishment2,
    Punishment3,
    Punishment4,
    ResultsWaitPage2,
    Results,
    FinalResultsWaitPage,
    FinalResults
]
