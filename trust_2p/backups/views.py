# -*- coding: utf-8 -*-
from __future__ import division

from otree.common import Currency as c, currency_range, safe_json

from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Welcome(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1
    
    form_model = models.Player
    form_fields = ['ethnic_in','religion_in']
    def vars_for_template(self):
        return {
            'exchange_rate': 0.4,
            }

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
    form_fields = ['question_trustA','question_trustB']

class Feedback_trust(Page):

    def is_displayed(self):
        return self.subsession.round_number == 1

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
            'tripled_amount': self.group.sent_amount * Constants.mult_factor
            }

    def sent_back_amount_choices(self):
        return currency_range(
            c(0),
            self.group.sent_amount * Constants.mult_factor,
            c(1)
            )

class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs_s1()

class FinalResultsWaitPage(WaitPage):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        self.group.set_payoffs_final()

class Results(Page):

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
            'player_in_all_rounds': self.player.in_all_rounds(),
            'paying_round': self.session.vars['paying_round']
            }

page_sequence = [
    Welcome,
    WelcomeTrust,
    Question_trust,
    Feedback_trust,
    Send,
    WaitForP1,
    SendBack,
    ResultsWaitPage,
    FinalResultsWaitPage,
    Results
]
