from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1

class Start(Page):
    def is_displayed(self):
        return self.round_number == 1

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'

class Period_Result(Page):
    def vars_for_template(self):
        p = self.player
        opponent_1 = p.opponent_1()
        opponent_2 = p.opponent_2()
        return dict(
            my_decision= p.decision,
            opponent_1_decision = opponent_1.decision,
            opponent_2_decision = opponent_2.decision,
            )

#class Result_round(Page):
    #pass
    #def is_displayed(self):
        #return self.round_number == [Constants.sub_rounds[i] for i in range(len(Constants.sub_rounds))] + 1

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [Introduction,Start,Decision, ResultsWaitPage, Period_Result, Results]
