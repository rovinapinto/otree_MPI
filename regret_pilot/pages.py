from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Block_1(Page):
    form_model = 'player'
    form_fields = ['decision_1']
   
class Decisions(Page):
	def vars_for_template(self):
		return dict(
			new_amount = self.player.decision_1+1,
			new_amount_less = self.player.decision_1-2,
			)

	form_model = 'player'
	form_fields = ['decision_2', 'decision_3', 'decision_4', 'decision_5', 'decision_6', 'decision_7']	

class Block_2(Page):
    form_model = 'player'
    form_fields = ['decision_8']

class Decisions_other(Page):
	def vars_for_template(self):
		return dict(
			new_amount = self.player.decision_8-1,
			new_amount_more = self.player.decision_8+2,
			)

	form_model = 'player'
	form_fields = ['decision_9', 'decision_10', 'decision_11', 'decision_12', 'decision_13', 'decision_14']

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [Block_1, Decisions, Block_2, Decisions_other,ResultsWaitPage, Results]
