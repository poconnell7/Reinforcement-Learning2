class Player:
    """Represents the base class for the algorithms (brute force and 
    reinforcement) and the Human User Interface"""
    
    def get_move(self, board, possible_moves, player_1_or_2):
           """Given the current board layout, a list of possible moves, 
        and the current player (1 or 2 =  -1)
        this will return one move from the list.
        def update_probabilities_as_game_is_over(self, final_result):
        It will return the index of the move in the list 
        of possible moves passed in.
        """
        
    def update_probabilities_as_game_is_over(self, final_result):
        """Placeholder for players that don't need this function i.e. UI and
        NegaMax. Only the Reinforcement Learning algorithm implements this 
        method. """