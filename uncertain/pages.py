from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants


class Question(Page):
    form_fields = ['n1', 'payoff_quest']
    form_model = 'player'


class Results(Page):
    pass


page_sequence = [Question, Results]
