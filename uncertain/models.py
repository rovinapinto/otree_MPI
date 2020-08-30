from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'uncertain'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    n1 = models.FloatField()
    payoff_quest = models.CurrencyField(initial=0) #need this in the currency field!!

    def total_pay(self):
        return self.payoff_quest.to_real_world_currency(self.session) # + self.participant.vars['payment'] 