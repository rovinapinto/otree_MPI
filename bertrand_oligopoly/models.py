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
#import random
#import numpy as np

author = 'Martin and Rovina'

doc = """
2 firms complete in a market by setting prices for homogenous goods.
See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):
    name_in_url = 'bertrand_oligopoly'
    players_per_group = 3
    num_rounds = 6 #total number of rounds
    sub_rounds = [2,4] #grouping after these rounds
    #sub_rounds = np.array(sub_rounds)

    instructions_template = 'bertrand/instructions.html'

    units = 24
    max_value = c(100)
    min_value = c(60)


class Subsession(BaseSubsession):
    def creating_session(self):
        for i in range(len(Constants.sub_rounds)): #np.arange(1,10,2) use arange!
            if self.round_number == Constants.sub_rounds[i] + 1:
                self.group_randomly()
                print(self.get_group_matrix())


    #need to add extra periods ex ante but in next button conditionally?
    #computer cooperation
    #random grouping - done except python modules not imported
    #random grouping with computer


class Group(BaseGroup):
    def set_payoffs(self):
        for p in self.get_players():
            p.set_payoff()

class Player(BasePlayer):
    decision = models.CurrencyField(
        choices=[60, 100],
        #doc="""This player's decision""",
        #widget=widgets.RadioSelect,
    )

    def opponent_1(self):
        return self.get_others_in_group()[0]
    def opponent_2(self):
        return self.get_others_in_group()[1]      

    def set_payoff(self):
        opponent_1 = self.get_others_in_group()[0]
        opponent_2 = self.get_others_in_group()[1]

        if self.decision == c(100):
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                self.payoff = Constants.max_value * (Constants.units/Constants.players_per_group)
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                self.payoff = c(0)
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                self.payoff = c(0)
            else:
                self.payoff = c(0)
        else:
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                self.payoff = Constants.min_value * Constants.units
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 1))
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 1))
            else:
                self.payoff = Constants.min_value * (Constants.units/Constants.players_per_group)
        return self.payoff    

    def units_sold(self):
        opponent_1 = self.get_others_in_group()[0]
        opponent_2 = self.get_others_in_group()[1]

        if self.decision == c(100):
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                self.units_sold = (Constants.units/Constants.players_per_group)
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                self.units_sold = 0
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                self.units_sold = 0
            else:
                self.units_sold = 0
        else:
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                self.units_sold = Constants.units
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                self.units_sold = (Constants.units/(Constants.players_per_group - 1))
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                self.units_sold = (Constants.units/(Constants.players_per_group - 1))
            else:
                self.units_sold = (Constants.units/Constants.players_per_group)
        return self.units_sold