#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 20:13:26 2019

@author: patrick
"""

from game_tic_tac_toe import Game
from human_ui import HumanUI
from reinforcement_learning import ReinforcementLearning

Game().start(ReinforcementLearning(1), HumanUI()) 
# Currently the RL algorithm has to be initialized with a player.
# We could change that, so it is done internally in the Game code, but
# the game position win probabilities stored by the RL algorithm depend
# on knowing which player is which.
# Consequently the player cannot be changed once the RL algorithm is initialized.