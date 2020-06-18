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
2 firms compete in a market by setting prices for homogenous goods.
See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):
    name_in_url = 'bertrand_oligopoly_bot'
    players_per_group = 2 # keep as it is for 2player + 1 bot game as it influences the grouping and shuffling
    team = 3 # 2players + 1bot --> only to calculate payoff and units sold
    
    #instructions_template = 'bertrand_oligopoly_bot/Instructions.html'

    units = 24
    max_value = c(100)
    min_value = c(60)

    inital_rounds = 2

    extra_period_1 = 2 
    extra_period_2 = 1
    extra_period_3 = 1

    super_round_1 = inital_rounds + extra_period_1 #no. of periods in each round
    super_round_2 = inital_rounds + extra_period_2
    super_round_3 = inital_rounds + extra_period_3

    num_rounds = super_round_1 + super_round_2 + super_round_3 #total no. of periods

    #for pages.py and final_payoff only --> to mark the boundary/end of rounds
    round_2 = super_round_1 + super_round_2
    round_3 = super_round_1 + super_round_2 + super_round_3


class Subsession(BaseSubsession):
    def creating_session(self):
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

class Group(BaseGroup):

    def cooperate(self):
        p1 = self.get_player_by_id(1) # id_in_group so same for each group in non-shuffled round
        p2 = self.get_player_by_id(2) #but how do i know if id ==1 corresponds to this player and not the opponent?
        if p1.decision == c(100) and p2.decision == c(100):
            return (2)
        elif p1.decision == c(60) and p2.decision == c(60):  
            return (1)
        else:
            return (0)

    def bot_decision(self):
        choice = np.float64(np.random.choice([100,60],size=1, p = [0.5,0.5]))
        #print("Choice made is ",choice)
        if self.round_number == 1 or self.round_number == (Constants.super_round_1 + 1) or self.round_number == (Constants.super_round_1 + Constants.super_round_2 +1):
            return 100 #plays high in the first period of each round
        else:
            if self.cooperate() == 2:
                return 100 # cooperates if both players cooperate
            elif self.cooperate() == 1:
                return 60
            else:
                return  60 # either cooperates or defects with a probabilty of 1/2

    # previous decision: self.player.in_round(self.round_number - 1).decision
    # call player and opponent: beware of shuffling groups- just call the players in a group. Role: self or opponent does not matter here. Decsion of both does
    # prob of 1/2: random.choice([a], p= [0.5]) or p = j/n-1 where j = no. of markets/players cooperate, n = no. of markets/players, p has to be same length as a 

class Player(BasePlayer):

    decision = models.CurrencyField(
        choices=[60, 100]
        )

    def opponent_1(self):
        return self.get_others_in_group()[0]           
   
    def units_sold(self):
        opponent_1 = self.get_others_in_group()[0]
        #opponent_2 = self.get_others_in_group()[1]
        bot_decision = self.group.bot_decision()

        if self.decision == c(100):
            if opponent_1.decision == c(100) and bot_decision == c(100):
                return (Constants.units/Constants.team)
            else:
                return 0
        else:
            if opponent_1.decision == c(100) and bot_decision == c(100):
                return Constants.units
            elif opponent_1.decision == c(100) and bot_decision == c(60):
                return (Constants.units/(Constants.team - 1))
            elif opponent_1.decision == c(60) and bot_decision == c(100):
                return (Constants.units/(Constants.team - 1))
            else:
                return (Constants.units/Constants.team)

    def set_payoff(self):
        opponent_1 = self.get_others_in_group()[0]
        bot_decision = self.group.bot_decision()
        print(bot_decision)
        if self.decision == c(100):
            if opponent_1.decision == c(100):
                if bot_decision == 100:
                    self.payoff = Constants.max_value * (Constants.units/Constants.team)
                else:
                    self.payoff = c(0)
            else:
                self.payoff = c(0)
        else:
            if opponent_1.decision == c(100):
                if bot_decision == 100:
                    self.payoff = Constants.min_value * Constants.units
                else:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 1))
            else:
                if bot_decision == 100:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 1))
                else:
                    self.payoff = Constants.min_value * (Constants.units / Constants.team)
        return self.payoff
        

    #select a random super_round and display the sum of that

    def round(self):
        return random.randint(1, 3)

    def final_payoff(self):
        p = self
        if self.round() == 1:
            return (sum([p.payoff for p in p.in_rounds(1, Constants.super_round_1)]))
        elif self.round() ==2:
            return (sum([p.payoff for p in p.in_rounds((Constants.super_round_1+1), Constants.round_2)]))
        else:
            return (sum([p.payoff for p in p.in_rounds((Constants.round_2+1), (Constants.round_3))]))   