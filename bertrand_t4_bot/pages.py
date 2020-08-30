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
    wait_for_all_groups = True
    after_all_players_arrive = 'set_payoffs'

class Period_Result(Page):
    def vars_for_template(self):
        p = self.player
        opponent_1 = p.opponent_1()
        opponent_2 = p.opponent_2()
        return dict(
            my_decision= p.decision,
            opponent_1_decision = opponent_1.decision,
            opponent_2_decision = opponent_2.decision
            )

class Result_round(Page):
    def is_displayed(self):
        if self.round_number == Constants.super_round_1:
            return True
        elif self.round_number == Constants.super_round_1 + Constants.super_round_2:
            return True
        elif self.round_number == Constants.super_round_1 + Constants.super_round_2 + Constants.super_round_3:
            return True
        else:
            return False 

    def vars_for_template(self):
        p = self.player
        if self.round_number == Constants.super_round_1:
            return {'round_payoff': sum([p.payoff for p in p.in_rounds(1, Constants.super_round_1)])
            }
        elif self.round_number == Constants.round_2:
            return {'round_payoff': sum([p.payoff for p in p.in_rounds((Constants.super_round_1+1), Constants.round_2)])
                }
        elif self.round_number == Constants.round_3:
            return {'round_payoff': sum([p.payoff for p in p.in_rounds((Constants.round_2+1), (Constants.round_3))])
            }
        else:
            return {'round_payoff': None}

class Results(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def vars_for_template(self):
        self.participant.payoff = self.player.final_payoff()
        self.participant.vars['payment'] = self.participant.payoff_plus_participation_fee()
        return {
            'payment': self.participant.vars['payment'],
            'rand_round': self.participant.vars['rand_round']
        }

page_sequence = [Introduction,Start,Decision, ResultsWaitPage, Period_Result, Result_round, Results]
