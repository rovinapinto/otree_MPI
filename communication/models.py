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

author = 'Rovina'

doc = """
Communication app: description to follow
"""


class Constants(BaseConstants):
    name_in_url = 'communication'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    def creating_session(self):
        for g in self.get_groups():
            g.case = random.choice([1,2,3,4])

class Group(BaseGroup):

    case = models.IntegerField(
        choices = [1,2,3,4] #has to be different for different groups chosen randomly and static. 
        )

    decision = models.IntegerField(
        choices=[1, 2], 
        label="Which option do you prefer?"
        ) 

    contribution_1 = models.CurrencyField(
        choices = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
        )

    contribution_2 = models.CurrencyField(
        choices = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50] 
        )

    project_1 = models.StringField(widget=widgets.RadioSelect, choices=[["X", 'X is available'],["Y", 'Only Y is available'],["Neither", 'Neither X nor Y are available (each participant gets 50 points)']],label="Please choose one of the following messages for Participant A:")
    project_2 = models.StringField(widget=widgets.RadioSelect, choices=[["X",'X is available'],["Neither", 'X is not available (each participant gets 50 points)']],label="Please choose one of the following messages for Participant A:")
    project_3 = models.StringField(widget=widgets.RadioSelect, choices=[["Y",'Y is available'],["Neither", 'Y is not available (each participant gets 50 points)']],label="Please choose one of the following messages for Participant A:")
    project_4 = models.StringField(widget=widgets.RadioSelect, choices=[["X",'X is available'],["Neither", 'X is not available (each participant gets 50 points)']],label="Please choose one of the following messages for Participant A:")
    project_5 = models.StringField(widget=widgets.RadioSelect, choices=[["X",'X is available'],["Neither", 'X is not available (each participant gets 50 points)']],label="Please choose one of the following messages for Participant A:")


    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        
        if self.case ==1: 
            if self.decision ==1 and self.contribution_1 != c(0):
                if self.project_1 == "X":
                    p1.payoff = c(300)
                    p2.payoff = -(self.contribution_1) + c(200)
                elif self.project_1 == "Y":
                    p1.payoff = c(130)
                    p2.payoff = -(self.contribution_1) + c(230)
                else:
                    p1.payoff = c(50)
                    p2.payoff = c(50) 
            elif self.decision ==2 and self.contribution_2 != c(0): 
                if self.project_1 == "X":
                    p1.payoff = c(300)
                    p2.payoff = -(self.contribution_2) + c(200)
                else:
                    p1.payoff = c(50)
                    p2.payoff = c(50) #check
            else:
                    p1.payoff = c(50)
                    p2.payoff = c(50)
        elif self.case == 2:
            if self.decision == 1 and self.contribution_1 != c(0): 
                if self.project_2 == "X":
                    p1.payoff = c(300)
                    p2.payoff = -(self.contribution_1) + c(200)
                else:
                    p1.payoff = c(50)
                    p2.payoff = c(50) #check
            elif self.decision == 2 and self.contribution_2 != c(0):
                if self.project_2 == "X":
                    p1.payoff = c(300)
                    p2.payoff = -(self.contribution_1) + c(200)
                else:
                    p1.payoff = c(50)
                    p2.payoff = c(50) #check
            else:
                p1.payoff = c(50)
                p2.payoff = c(50)
        elif self.case == 3:
            if self.decision == 1 and self.contribution_1 != c(0):
                if self.project_3 == "Y":
                    p1.payoff = c(130)
                    p2.payoff = -(self.contribution_1) + c(230)
                else:
                    p1.payoff = c(50)
                    p2.payoff = c(50) #check
            else:
                p1.payoff = c(50)
                p2.payoff = c(50)
        else: 
            p1.payoff = c(50)
            p2.payoff = c(50)


        return p1.payoff, p2.payoff #run this method set_payoff to receive the payoffs ---> runs in pages.py

    def project(self):
        if self.case ==1: 
            if self.decision == 1: 
                if self.project_1 == "X":
                    project = "X" 
                elif self.project_1 == "Y":
                    project = "Y"
                else:
                    project = "Neither"
            else:  
                if self.project_4 == "X":
                    project = "X"
                else:
                    project = "Neither"
        elif self.case == 2:
            if self.decision == 1: 
                if self.project_2 == "X":
                    project = "X"
                else:
                    project = "Neither"
            else: 
                if self.project_5 == "X":
                    project = "X"
                else:
                    project = "Neither"
        elif self.case == 3:
            if self.decision == 1:
                if self.project_3 == "Y":
                    project = "Y"
                else:
                    project = "Neither"
            else:
                project = "Neither"
        else: 
            project = "Neither"
            #print("this keeps going down")

        return project 


class Player(BasePlayer):

    def role(self):
        if self.id_in_group == 1:
            return 'Participant A' 
        if self.id_in_group == 2:
            return 'Participant B'

    def endowment(self):
        if self.id_in_group == 1: #write in terms of player roles instead??
             endowment = 50
        if self.id_in_group == 2: 
             endowment = 100 
        return endowment
    
    
    #Conversion of payoff to euros?


