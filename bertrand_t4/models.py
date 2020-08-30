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
import numpy as np
import random

author = 'Martin and Rovina'

doc = """
Treatment with 4 players.
2 firms compete in a market by setting prices for homogenous goods.
See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):
    name_in_url = 'bertrand_oligopoly_4player'
    players_per_group = 4
    
    instructions_template = 'bertrand_t4/Instructions.html'

    units = 24
    max_value = c(100)
    min_value = c(60)

    inital_rounds = 2

    extra_period_1 = 2
    extra_period_2 = 1
    extra_period_3 = 1

    super_round_1 = inital_rounds + extra_period_1
    super_round_2 = inital_rounds + extra_period_2
    super_round_3 = inital_rounds + extra_period_3

    num_rounds = super_round_1 + super_round_2 + super_round_3

    #for pages.py and final_payoff only
    round_2 = super_round_1 + super_round_2
    round_3 = super_round_1 + super_round_2 + super_round_3


class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players(): #random number for each participant for the final payoff
            p.participant.vars['rand_round'] = random.randint(1,3)
        
        if self.round_number == (Constants.super_round_1 +1):
            self.group_randomly()
            print(self.get_group_matrix())
        elif self.round_number > (Constants.super_round_1 +1) and self.round_number < (Constants.super_round_1 + Constants.super_round_2 +1):
            self.group_like_round(Constants.super_round_1 +1)
        elif self.round_number == (Constants.super_round_1 + Constants.super_round_2 +1):
            self.group_randomly()
            print(self.get_group_matrix())
        elif self.round_number > (Constants.super_round_1 + Constants.super_round_2 +1):
            self.group_like_round(Constants.super_round_1 + Constants.super_round_2 +1)
        else:
            self.group_like_round(1)    

    def set_payoffs(self):
        for p in self.get_players():
            p.set_payoff()

    #computer cooperation
    #random grouping - test complete
    #random grouping with computer


class Group(BaseGroup):
    pass

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
    def opponent_3(self):
        return self.get_others_in_group()[2]      

    def set_payoff(self):
        opponent_1 = self.get_others_in_group()[0]
        opponent_2 = self.get_others_in_group()[1]
        opponent_3 = self.get_others_in_group()[2]

        if self.decision == c(100):
            if opponent_1.decision == c(100) and opponent_2.decision == c(100) and opponent_3.decision == c(100):
                self.payoff = Constants.max_value * (Constants.units/Constants.players_per_group)
            else:
                self.payoff = c(0)
        else:
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                if opponent_3.decision == c(100):
                    self.payoff = Constants.min_value * Constants.units
                else:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 2))
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                if opponent_3.decision == c(100):
                    self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 2))
                else:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 1))
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                if opponent_3.decision == c(100):
                    self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 2))
                else:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 1))
            else:
                if opponent_3.decision == c(100):
                    self.payoff = Constants.min_value * (Constants.units/(Constants.players_per_group - 1))
                else:
                    self.payoff = Constants.min_value * (Constants.units/Constants.players_per_group)
        return self.payoff    

    def units_sold(self):
        opponent_1 = self.get_others_in_group()[0]
        opponent_2 = self.get_others_in_group()[1]
        opponent_3 = self.get_others_in_group()[2]

        if self.decision == c(100):
            if opponent_1.decision == c(100) and opponent_2.decision == c(100) and opponent_3.decision == c(100):
                return (Constants.units/Constants.players_per_group)
            else:
                return 0
        else:
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                if opponent_3.decision == c(100):
                    return Constants.units
                else:
                    return (Constants.units/(Constants.players_per_group - 2))
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                if opponent_3.decision == c(100):
                    return (Constants.units/(Constants.players_per_group - 2))
                else:
                    return (Constants.units/(Constants.players_per_group - 1))
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                if opponent_3.decision == c(100):
                    return (Constants.units/(Constants.players_per_group - 2))
                else:
                    return (Constants.units/(Constants.players_per_group - 1))
            else:
                if opponent_3.decision == c(100):
                    return (Constants.units/(Constants.players_per_group - 1))
                else:
                    return (Constants.units/Constants.players_per_group)


    #display the sum of the random super round and compute payoff

    def final_payoff(self):
        p = self
        if self.participant.vars['rand_round'] == 1:
            return (sum([p.payoff for p in p.in_rounds(1, Constants.super_round_1)]))
        elif self.participant.vars['rand_round'] == 2:
            return (sum([p.payoff for p in p.in_rounds((Constants.super_round_1+1), Constants.round_2)]))
        else:
            return (sum([p.payoff for p in p.in_rounds((Constants.round_2+1), (Constants.round_3))]))  

