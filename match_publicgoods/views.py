# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random

class WelcomePublicGoods(Page):
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
            'payoff_ex_low': Constants.endowment * ((Constants.players_per_group - 1)* 0.3 + 0.5) * (Constants.effic_factor / Constants.players_per_group)
            }

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

    # This method is used to obtain the ethnicity of each participant to be shown in the contribution stage
    def vars_for_template(self):
       p1 = self.group.get_player_by_id(1)
       p2 = self.group.get_player_by_id(2)
       p3 = self.group.get_player_by_id(3)
       p4 = self.group.get_player_by_id(4)
       p1.ethnicity = p2.get_others_in_group()[0].participant.vars['ethnic']
       p2.ethnicity = p1.get_others_in_group()[0].participant.vars['ethnic']
       p3.ethnicity = p1.get_others_in_group()[1].participant.vars['ethnic']
       p4.ethnicity = p1.get_others_in_group()[2].participant.vars['ethnic']
       return {
           'ethnicity_p1': p1.ethnicity,
           'ethnicity_p2': p2.ethnicity,
           'ethnicity_p3': p3.ethnicity,
           'ethnicity_p4': p4.ethnicity,
           }

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs_s1()

# !!! One problem so far with the page Punishment.html is that for every player
# is shown the punishment decision for himself (which should be zero always)
# Is there a way to set punish_pK for player K in zero and do not display it?

class Results(Page):
    pass

class FinalResults(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    # Computation of the cumulative earnings of the public goods game
    # This cumulative earnings are defined as payoff_block2
    def vars_for_template(self):
        # There may be a way to use a nested loop to get payoff_block2
        p1 = self.group.get_player_by_id(1)
        p2 = self.group.get_player_by_id(2)
        p3 = self.group.get_player_by_id(3)
        p4 = self.group.get_player_by_id(4)
        player_in_all_rounds = self.player.in_all_rounds()
        p1.payoff_block2 = sum([p.prepayoff for p in player_in_all_rounds])
        p2.payoff_block2 = sum([p.prepayoff for p in player_in_all_rounds])
        p3.payoff_block2 = sum([p.prepayoff for p in player_in_all_rounds])
        p4.payoff_block2 = sum([p.prepayoff for p in player_in_all_rounds])
        # !!! The variable payoff_block2 is being properly displayed, but it is not properly stored
        # !!! It stores the prepayoff of one of the four group members
        return {'payoff_block2': self.player.payoff_block2}


page_sequence = [
    # WelcomePublicGoods,
    ShuffleWaitPage,
    Contribute,
    ResultsWaitPage,
    Results,
    FinalResults
]

