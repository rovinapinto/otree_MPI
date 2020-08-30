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
import numpy as np
import random

author = 'Martin and Rovina'

doc = """
Treatment 4 with bot.
2 firms compete in a market by setting prices for homogenous goods.
See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):

    name_in_url = 'bertrand_t4_bot'
    players_per_group = 3 # keep as it is for 3 player + 1 bot game as it influences the grouping and shuffling
    team = 4 # 2players + 1bot --> only to calculate payoff and units sold
    
    #instructions_template = 'bertrand_t4_bot/Instructions.html'

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


class Subsession(BaseSubsession): #executes the functions at the start of the session ie for all rounds at once
    def creating_session(self): #random grouping for each super_round    
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

        for g in self.get_groups(): #generating random number for each group 
            g.prob_high = np.int_(random.choices([100,60],k=1, weights = [2/3,1/3])) 
            g.prob_low = np.int_(random.choices([100,60],k=1, weights = [1/3,2/3])) 


    def set_payoffs(self):
        for p in self.get_players():
            p.set_payoff()

class Group(BaseGroup): 

    prob_high = models.IntegerField(
        choices = [100,60]
        )
    prob_low = models.IntegerField(
        choices = [100,60]
        )

    def count(self): #use the number/count of highs and lows to decide on bot decision
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)

        choices_made = []
        choices_made.append(p1.in_round(self.round_number - 1).decision)
        choices_made.append(p2.in_round(self.round_number - 1).decision)
        choices_made.append(p3.in_round(self.round_number - 1).decision)
        print(choices_made)
        print(choices_made.count(100))

        return choices_made.count(100)

    def bot_decision(self):
        if self.round_number == 1 or self.round_number == (Constants.super_round_1 + 1) or self.round_number == (Constants.super_round_1 + Constants.super_round_2 +1):
            return 100 #plays high in the first period of each round
        else:
            if self.count() == 3:
                return 100 # cooperates if all 3 players cooperate
            elif self.count() == 0:
                return 60
            elif self.count()== 2:
                return self.prob_high
            else:
                return self.prob_low 

    # previous decision: self.player.in_round(self.round_number - 1).decision
    # call player and opponent: beware of shuffling groups- just call the players in a group. Role: self or opponent does not matter here. Decsion of both does
    # prob: random.choice([a], p= [0.5]) or p = j/n-1 where j = no. of markets/players cooperate, n = no. of markets/players, p has to be same length as a 

class Player(BasePlayer):

    decision = models.CurrencyField(
        choices=[60, 100]
        )

    def opponent_1(self): #required for pages.py
        return self.get_others_in_group()[0]
    def opponent_2(self):
        return self.get_others_in_group()[1]          
   
    def units_sold(self):
        opponent_1 = self.get_others_in_group()[0]
        opponent_2 = self.get_others_in_group()[1]
        bot_decision = self.group.bot_decision()
        print(bot_decision)

        if self.decision == c(100):
            if opponent_1.decision == c(100) and opponent_2.decision == c(100) and bot_decision == c(100):
                return (Constants.units/Constants.team)
            else:
                return 0
        else:
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                if bot_decision == c(100):
                    return Constants.units
                else:
                    return (Constants.units/(Constants.team - 2))
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                if bot_decision == c(100):
                    return (Constants.units/(Constants.team - 2))
                else:
                    return (Constants.units/(Constants.team - 1))
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                if bot_decision == c(100):
                    return (Constants.units/(Constants.team - 2))
                else:
                    return (Constants.units/(Constants.team - 1))
            else:
                if bot_decision == c(100):
                    return (Constants.units/(Constants.team - 1))
                else:
                    return (Constants.units/Constants.team)

    #compute the payoff based on group and bot decisions
    def set_payoff(self):
        opponent_1 = self.get_others_in_group()[0]
        opponent_2 = self.get_others_in_group()[1]
        bot_decision = self.group.bot_decision()

        if self.decision == c(100):
            if opponent_1.decision == c(100) and opponent_2.decision == c(100) and bot_decision == c(100):
                self.payoff = Constants.max_value * (Constants.units/Constants.team)
            else:
                self.payoff = c(0)
        else:
            if opponent_1.decision == c(100) and opponent_2.decision == c(100):
                if bot_decision == c(100):
                    self.payoff = Constants.min_value * Constants.units
                else:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 2))
            elif opponent_1.decision == c(100) and opponent_2.decision == c(60):
                if bot_decision == c(100):
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 2))
                else:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 1))
            elif opponent_1.decision == c(60) and opponent_2.decision == c(100):
                if bot_decision == c(100):
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 2))
                else:
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 1))
            else:
                if bot_decision == c(100):
                    self.payoff = Constants.min_value * (Constants.units/(Constants.team - 1))
                else:
                    self.payoff = Constants.min_value * (Constants.units/Constants.team)
        return self.payoff
        

    #display the sum of the random super round and compute payoff

    def final_payoff(self):
        p = self
        if self.participant.vars['rand_round'] == 1:
            return (sum([p.payoff for p in p.in_rounds(1, Constants.super_round_1)]))
        elif self.participant.vars['rand_round'] == 2:
            return (sum([p.payoff for p in p.in_rounds((Constants.super_round_1+1), Constants.round_2)]))
        else:
            return (sum([p.payoff for p in p.in_rounds((Constants.round_2+1), (Constants.round_3))]))