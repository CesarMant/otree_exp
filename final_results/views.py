# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class ResultsWaitPage(WaitPage):

    def is_displayed(self):
        for player in self.subsession.get_players():
            player.payoff_block1 = player.participant.vars['payoff_block1']
            player.payoff_block2 = player.participant.vars['payoff_block2']
            player.set_final_payoff()


class Final_Payment(Page):

    def vars_for_template(self):
        return{
            'payoff_block1' : self.player.payoff_block1,
            'payoff_block2' : self.player.payoff_block2,
            'exchange_rate': 0.4,
            'payoff_yuan': self.player.payoff * 0.4,
            'show_up': 50,
            'final_earnings': self.player.payoff * 0.4 + 50,
        }


page_sequence = [
    ResultsWaitPage,
    Final_Payment
]
