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


doc = """
2 firms complete in a market by setting prices for homogenous goods.
See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class Constants(BaseConstants):
    players_per_group = 3
    name_in_url = 'market_game'
    num_rounds = 20

    instructions_template = 'bertrand/instructions.html'

    # payoff if all play high""",
    player_high_hhh_payoff = c(800)

    # payoff if 2 players play high and the other low""",
    player_low_lhh_payoff = c(1440)
    player_high_lhh_payoff = c(0)


    # payoff if 2 players play low and the other high""",
    player_low_llh_payoff = c(720)
    player_high_llh_payoff = c(0)

    # payoff if all play low""",
    player_low_lll_payoff = c(480)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    winning_price = models.CurrencyField()

    def set_payoffs(self):
        import random

        players = self.get_players()
        self.winning_price = min([p.price for p in players])
        winners = [p for p in players if p.price == self.winning_price]
        winner = random.choice(winners)

        for p in players:
            if p == winner:
                p.is_winner = True
                p.payoff = p.price
            else:
                p.is_winner = False
                p.payoff = c(0)


class Player(BasePlayer):
    decision = models.CurrencyField(
        min= 60,
        max= 100,
        doc="""This player's decision""",
        widget=widgets.RadioSelect,
    )

    def other_player_1(self):
        return self.get_others_in_group()[0]

    def other_player_2(self):
        return self.get_others_in_group()[0]

    def set_payoff(self):
        payoff_matrix = dict(
            High=dict(
                All_High=Constants.player_high_hhh_payoff,
                One_low =Constants.player_high_lhh_payoff,
                Two_low =Constants.player_high_llh_payoff
            ),
            Low=dict(
                One_low=Constants.player_low_lhh_payoff,
                Two_Low=Constants.player_low_llh_payoff,
                All_Low=Constants.player_low_lll_payoff
            ),
        )

        self.payoff = payoff_matrix[self.decision][self.other_player_1().decision][self.other_player_2().decision]