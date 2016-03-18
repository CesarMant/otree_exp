# -*- coding: utf-8 -*-
from __future__ import division

import random

from otree.common import Currency as c, currency_range

from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):
    """Bot that plays one round"""

    def play_round(self):
        self.submit(views.Welcome,{'ethnic_in': random.choice(['Dai','Han']),
                                   'religion_in': random.choice(['Buddhist','Christian'])})
        if self.player.id_in_group == 1:
            self.submit(views.Send,{'sent_amount': 8})
        elif self.player.id_in_group == 2:
            self.submit(views.Send)

        if self.player.id_in_group == 2:
            self.submit(views.SendBack,{'sent_back_amount': 10})
        elif self.player.id_in_group == 1:
            self.submit(views.SendBack)

        self.submit(views.Results)

    def validate_play(self):
        pass
