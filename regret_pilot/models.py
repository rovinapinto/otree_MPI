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
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'regret_pilot'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_players():
            g.computer_1 = random.choice([5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]) #equal probabilty code
            g.computer_2 = random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
            g.decisions = random.choice([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14])


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    computer_1 = models.IntegerField(
        choices = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] 
        )
    computer_2 = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        )
    decisions = models.IntegerField(
        choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14]
        )

    #need to execute lottery 10 times: lottery[0] lottery[9] against decision_x

    #set_payoffs for each decision? or a way to add plu/minus using vars?

    def set_payoffs(self):
        if self.lottery == 1:
            player.payoff = self.decision_1
        else:
            player.payoff = 5

    def make_field_1(label):
        return models.IntegerField(
            choices=[5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            label=label
            )
    def make_field_2(label):
        return models.IntegerField(
            choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
            label=label
            )
    def contribute(label):
        return models.FloatField(
            max=10, min=0, label = label)

    def bool_field():
        return models.BooleanField(
        choices=[
            [True, 'Left'],
            [False, 'Right'], 
        ],
        label="Which option do you prefer?"
        )

    decision_1 = make_field_1("What is the smallest amount of money x such that you would prefer to play the lottery than to earn 5€ for sure?")
    decision_2 = bool_field()
    decision_3 = bool_field()
    decision_4 = contribute("How much would you be willing to pay in order not to know the outcome of the lottery?")
    decision_5 = bool_field()
    decision_6 = bool_field()
    decision_7 = contribute("How much would you be willing to pay in order to know the outcome of the lottery?")
    decision_8 = make_field_2("What is the smallest amount of money y such that you would prefer to earn y€ for sure than to play the lottery?")
    decision_9 = bool_field()
    decision_10 = bool_field()
    decision_11 = contribute("How much would you be willing to pay in order not to know the outcome of the lottery?")
    decision_12 = bool_field()
    decision_13 = bool_field()
    decision_14 = contribute("How much would you be willing to pay in order to know the outcome of the lottery?")



    #payoff: if decision_1 is < computer then payoff is c(5) else play lottery
