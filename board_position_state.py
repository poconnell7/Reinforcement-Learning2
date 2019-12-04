class BoardPositionState:
    """ Stores and updates the win probability for each possible board layout"""

    def __init__(self):
               
        # Assume win, draw or loss are all equally likely = 33%
        self.win_probability = 1/3 # Initial default probability of 
        # winning from this position, assuming this is not a won or lost 
        # board position. For won or lost position it should be 1 or 0 respectively.

        self.draw_probability = 1/3
        
        self.learning_rate = 0.2 # somewhat arbitrarily chosen small positive fraction,
        # aka step-size parameter, which influences the rate of learning.

    def get_win_probability(self):
        return self.win_probability
    
    def get_draw_probability(self):
        return self.draw_probability
    
    def update_probabilities_after_win(self):
        # This is called when a move we make wins the game i.e. the game position
        # resulting from this move has a 100% probability of a win for us.
        self.win_probability = 1
        self.draw_probability = 0 # 100% chance of a win => 0% chance of a draw
        # This is not necessarily true for a game resulting in a draw or loss 
        # i.e. a draw/loss (usually) requires a move by the other player, so 
        # the result of our move/new board position depends on what the opponent does.
        
    def update_win_probability_based_on_next_outcome(self, outcome):
        # The parameter 'outcome' is a value between 0 and 1 which 
        # represents the probability of a win in the board position we moved
        # to after this one.
        # We use it to calculate the probability of a win from 
        # this position, by moving this probability closer to the next one,
        # i.e. closer to the one which has a result = win/draw/loss.
        #win_prob = self.win_probability
        difference = outcome - self.win_probability
        self.win_probability += self.learning_rate * (difference)
        # The effect of this is to move the current board win probability
        # closer to the win probability of the board position after our next move.
        # This is referred to as backing up the value to the state before the move
        
    def update_draw_probability_based_on_next_outcome(self, outcome):
        # The parameter 'outcome' is a value between 0 and 1 which 
        # represents the probability of a draw in the board position we moved
        # to after this one.
        # We use it to calculate the probability of a draw from 
        # this position, by moving this probability closer to the next one,
        # i.e. closer to the one which has a result = win/draw/loss.        
        difference = outcome - self.draw_probability
        self.draw_probability += self.learning_rate * (difference)
        
    def get_win_draw_prob_value(self):
        # This returns a value based on the win and draw probabilities
        # Assume a win is worth twice as much as a draw
        win_vs_draw_multiplier = 2
        win_draw_prob_value = (win_vs_draw_multiplier * self.win_probability)\
                                + self.draw_probability
                
        return win_draw_prob_value
    
    def __str__(self): # Must return string (for printing etc)
        return 'class BoardPositionState - Constr. win_probability: ' \
                + str(self.win_probability)

