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
    
    instructions_template = 'bertrand_oligopoly_bot/Instructions.html'

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
        print ("Is this running in subsession")

    #computer cooperation
    #random grouping with computer


class Group(BaseGroup):
    pass
    # previous decision: self.player.in_round(self.round_number - 1).decision
    # call player and opponent: beware of shuffling groups
    # prob of 1/2: random.choice([a], p= 0.5) or p = j/n-1 where j = no. of markets/players cooperate, n = no. of markets/players 
 
class Player(BasePlayer):
    decision = models.CurrencyField(
        choices=[60, 100]
        )

    def opponent_1(self):
        return self.get_others_in_group()[0] 

    def bot_decision(self):
        if self.round_number == 1 or self.round_number == (Constants.super_round_1 + 1) or self.round_number == (Constants.super_round_1 + Constants.super_round_2 +1):
            self.bot_decision = c(100)
        else:
            self.bot_decision = c(60)  
        return self.bot_decision            
   

    def units_sold(self):
        opponent_1 = self.get_others_in_group()[0]
        #opponent_2 = self.get_others_in_group()[1]

        if self.decision == c(100):
            if opponent_1.decision == c(100) and self.bot_decision == c(100):
                self.units_sold = (Constants.units/Constants.team)
            else:
                self.units_sold = 0
        else:
            if opponent_1.decision == c(100) and self.bot_decision == c(100):
                self.units_sold = Constants.units
            elif opponent_1.decision == c(100) and self.bot_decision == c(60):
                self.units_sold = (Constants.units/(Constants.team - 1))
            elif opponent_1.decision == c(60) and self.bot_decision == c(100):
                self.units_sold = (Constants.units/(Constants.team - 1))
            else:
                self.units_sold = (Constants.units/Constants.team)
        return self.units_sold

    def set_payoff(self):
        opponent_1 = self.get_others_in_group()[0]
        #opponent_2 = self.get_others_in_group()[1]

        if self.decision == c(100):
            if opponent_1.decision == c(100) and self.bot_decision == c(100):
                self.payoff = (Constants.units/Constants.team)
            else:
                self.payoff = c(0)
        else:
            if opponent_1.decision == c(100) and self.bot_decision == c(100):
                self.payoff = Constants.units
            elif opponent_1.decision == c(100) and self.bot_decision == c(60):
                self.payoff = (Constants.units/(Constants.team - 1))
            elif opponent_1.decision == c(60) and self.bot_decision == c(100):
                self.payoff = (Constants.units/(Constants.team - 1))
            else:
                self.payoff = (Constants.units/Constants.team)
        print ("Is this running in player")        
        return self.payoff
        

    #select a random super_round and display the sum of that

    def round(self):
        self.round = random.randint(1, 3)
        print (self.round) 
        return self.round

    def final_payoff(self):
        p = self
        if self.round == 1:
            final_payoff = sum([p.payoff for p in p.in_rounds(1, Constants.super_round_1)])
        elif self.round ==2:
            final_payoff = sum([p.payoff for p in p.in_rounds((Constants.super_round_1+1), Constants.round_2)])
        else:
            final_payoff = sum([p.payoff for p in p.in_rounds((Constants.round_2+1), (Constants.round_3))])
        return final_payoff    
'''
    def cooperate(self):
        p = self.get_player_by_id(1) # id_in_group so same for each group in non-shuffled round
        opponent_1 = self.get_player_by_id(2) #but how do i know if id ==1 corresponds to this player and not the opponent?
        if self.p.decision == c(100) and opponent_1.decision == c(100):
            self.cooperate = 2
        elif self.p.decision == c(60) and opponent_1.decision == c(60):  
            self.cooperate = 1
        else:
            self.cooperate = 0

    def bot_decision(self):
        if self.round_number == 1 or self.round_number == (Constants.super_round_1 + 1) or self.round_number == (Constants.super_round_1 + Constants.super_round_2 +1):
            self.bot_decision = c(100) #plays high in the first period of each round
        else:
            if self.cooperate == 2:
                self.bot_decision = c(100) # cooperates if both players cooperate
            if self.cooperate == 1:
                self.bot_decision = c(60)
            else:
                self.bot_decision =  c(np.random.choice([100,60], p = 0.5))  # either cooperates or defects with a probabilty of 1/2
'''