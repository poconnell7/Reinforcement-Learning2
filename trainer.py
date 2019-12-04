#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 00:51:41 2019

@author: patrick
"""

from game_tic_tac_toe import Game

class Trainer:
    """Executes multiple games for the two players passed in.
    This is used to train the Reinforcement Learning algorithm.
    """
    
    def start(self, player1, player2, number_of_games):
        """Starts the loop that executes the games"""
        
#        for game_number in range(number_of_games):
            # first game number will be zero
        for _ in range(number_of_games):
            # game number is not used/needed
            
            Game().start(player1, player2)
            
        # Return the players which contain the win/loss record
        # and, for the RL algorithm, the trained 'policy'
        return player1, player2
        # Returning these may be unnecessary as the calling program probably 
        #still has a reference to them
            