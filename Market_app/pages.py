from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class MyPage(Page):
    pass

class Introduction(Page):
    pass

class Start(Page):
    pass

class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']
    pass

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass

class Period_Result(Page):
    def vars_for_template(self):
        me = self.player
        opponent_1 = me.other_player_1()
        opponent_2 = me.other_player_2()
        return dict(
            my_decision=me.decision,
            opponent_1_decision=opponent_1.decision,
            opponent_2_decision=opponent_1.decision,
            same_choice=me.decision == opponent_1.decision == opponent_2.decision,)




page_sequence = [Introduction,Start,Decision, ResultsWaitPage, Period_Result]
