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
Demographics for the bertrand oligopoly experiment
"""


class Constants(BaseConstants):
    name_in_url = 'demographics'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="Wie alt sind Sie?", min=15, max=99)
    gender = models.StringField(label="Welches Geschlecht haben Sie?",
                                    choices=["weiblich", "männlich", "divers"],
                                    widget=widgets.RadioSelect)
    employment = models.StringField(label="Welcher Beschäftigung gehen Sie gerade hauptsächlich nach?",
                                        choices=["Schüler*in",
                                                 "In Ausbildung",
                                                 "Student*in",
                                                 "Angestellte*r",
                                                 "Beamte*r",
                                                 "Selbstständig",
                                                 "Arbeitslos/Arbeit suchend",
                                                 "Im Ruhestand",
                                                 "Einer anderen"],
                                        widget=widgets.RadioSelect)
    subject = models.StringField(label="Falls Sie studieren, welches Fach studieren Sie im Hauptfach?", blank=True,
                                     choices=["Kulturwissenschaften",
                                             "Sprachwissenschaften",
                                              "Philosophie & sonstige Geisteswissenschaften",
                                                "Pädagogik & Erziehungswissenschaften",
                                               "Rechtswissenschaften",
                                              "Wirtschaftswissenschaften",
                                              "Sozial- und Politische Wissenschaften",
                                              "Medizin & Pflegewissenschaften",
                                              "Land- und Forstwissenschaften",
                                              "Mathematisch-naturwissenschaftliche Fächer",
                                              "Technische Wissenschaften",
                                              "Kunst oder Musik",
                                              "Sonstiges",
                                              "Ich studiere nicht"],
                                     widget=widgets.RadioSelect)

    anmerkungen = models.LongStringField() 
