# oTree experiments
## Some otree experiments written for MPI Collective Goods, Bonn.

The main code is for a Bertrand oligopoly market/ prisoner’s dilemma game. There are 6 apps to this game:
  - 3 player game
  - 4 player game
  - 2 player and 1 bot game
  - 3 player and 1 bot game
  - demographics
  - uncertain
  
What you will find in the above betrand_* apps are how to :
  - shuffle players for different rounds
  - define functions in group and player class
  - integrate a 'bot' or define function to make decisions based on the player's decision
  - use previous rounds for calculations
  - defining vars_for_template() to use in pages 
  - select a random round for each participant for the payoff 
  - create a random number 
  - generate weighted numbers for groups with given probability 
  - take the sum of all rounds and sum of particular rounds
  - implement other apps in the same game- see demographics and uncertain
  - use particiapnt.vars to carry data from one app to another
  - convert ECU to real currency
  - create a slider in the html page- see uncertain
  
For more details on how to use oTree, please see:
https://otree.readthedocs.io/en/latest/
https://groups.google.com/g/otree

