from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class Screen_1_choice(Page):

    form_model = 'group'
    form_fields = ['decision']

    def is_displayed(self):
        return self.player.id_in_group == 1

#class WaitForP_A(WaitPage):
    #pass


class Screen_1(Page):

    def is_displayed(self):
        return self.player.id_in_group == 2


class Screen_2(Page):
    form_model = "group"
    form_fields = ['contribution_1', 'project_1', 'project_2', 'project_3', 'contribution_2','project_4', 'project_5']

    def is_displayed(self):
        return self.player.id_in_group == 2
'''
class screen_2_result(Page):

    form_model = "group" 
    form_fields = ['project_1', 'project_2', 'project_3']

    def is_displayed(self):
        return self.player.id_in_group == 2

class screen_3(Page):

    form_model = "group" 
    form_fields = ['project_1', 'project_2', 'project_3']

    def is_displayed(self):
        return self.player.id_in_group == 2

class screen_4(Page):

    form_model = "group" 
    form_fields = ['contribution_2']

    def is_displayed(self):
        return self.player.id_in_group == 2

class screen_4_result(Page):

    def is_displayed(self):
        return self.player.id_in_group == 2

class screen_5(Page):

    form_model = "group" 
    form_fields = ['project_4', 'project_5']

    def is_displayed(self):
        return self.player.id_in_group == 2

'''        

class ResultsWaitPage(WaitPage):
    #def after_all_players_arrive(self):
        #for p in self.group.get_players(): #self.group.set_payoffs()
            #p.set_payoffs()
        
    after_all_players_arrive = 'set_payoffs'

class Results(Page):
    pass


page_sequence = [Screen_1_choice, Screen_1, Screen_2, ResultsWaitPage, Results]
