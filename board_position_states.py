import numpy as np
from game_type import GameType
from board_position_state import BoardPositionState

class BoardPositionStates(GameType):
    """Contains a collection of BoardPositionState instances. 
    Calculates the next move based on the win probabilities of each 
    possible resultant board position."""
    
    def __init__(self):
        #super().__init__() # Currently not necessary
        self.position_states_dictionary = {}
        
    def get_state(self, board_position):
        """Returns the 'state' for this board position which contains
        the currently calculated likelihood of winning or 
        drawing from this position."""
        
        board_key = self.two_dim_array_to_tuple(board_position) # np arrays are not hashable
        # So convert two dimensional array to two dimensional tuple, 
        # so it can be used as a key in dictionary.
                
        if board_key in self.position_states_dictionary:
            current_position_state = self.position_states_dictionary[board_key]
        else: # create new Board Position State instance with default values for win/draw 
            current_position_state = BoardPositionState()

            # Store it in a dictionary
            self.position_states_dictionary[board_key] = current_position_state 
                            
        return current_position_state
     
    def get_win_draw_prob_value(self, board):
        return self.get_state(board).get_win_draw_prob_value()
    
    def get_next_move(self, board, all_possible_moves, player_1_or_2):

        # This picks the next move using the current win/draw probabilities stored
        # for each resulting board position. It is "random", but positions which
        # currently have higher probabilites of leading to a win (or draw), are more
        # likely to be chosen.
        # Second parameter, player_1_or_2, is 1 or -1, depending on who's move it is
        
        all_possible_win_draw_probabilities = {} 
        # key will be board; value=win probability
        
        for i,j in all_possible_moves:
            # Use i,j below to reset the board by setting this back to zero 
            # after we have determined which move is best - to avoid changing
            # the board in the calling function.
            # Update the board with each possible move to determine which is best
            board[i,j] = player_1_or_2 # 1 or -1, depending on who's move it is
            
            current_board_state = self.get_state(board)

            current_board_win_draw_prob = current_board_state.get_win_draw_prob_value()

            current_board_key = self.two_dim_array_to_tuple(board)
            
            # We could also have used the move i,j as the key here. 
            # That might have been simpler i.e at end we need to retrieve the move
            all_possible_win_draw_probabilities[current_board_key] = \
                current_board_win_draw_prob
              
            board[i,j] = 0 # reset the board to the way it was, before this move
            # i.e. undo this move; so we don't affect the next iteration of this
            # loop, or potentially, the caller of this function.
                        
        # We are using np.random.choice below which requires an array-like
        # input parameter for "p". So convert dictionary values to np array.
        all_possible_win_draw_probabilities_values = \
            np.array(list(all_possible_win_draw_probabilities.values()))
                        
        # The sum of all the probabilities of all the possible moves need
        # to sum to one, before passing to np.random.choice.
        # So divide each value by the sum
        sum_all_probabilities = all_possible_win_draw_probabilities_values.sum()
                
        move_relative_probabilities = \
            all_possible_win_draw_probabilities_values/sum_all_probabilities        

        all_possible_win_draw_probabilities_keys = \
            np.array(list(all_possible_win_draw_probabilities.keys()))
                            
        number_of_keys = len(all_possible_win_draw_probabilities_keys)
                
        all_possible_win_draw_probabilities_keys_indexes = np.arange(number_of_keys)

        
        selected_move = np.random.choice(\
                     all_possible_win_draw_probabilities_keys_indexes,\
                     p = move_relative_probabilities)
        # np.random.choice requires that the "p" parameter be a "true" list

        # For now we only ever get one selected move. 
        #first_selected_move = all_possible_moves[selected_move]
#        first_selected_move = all_possible_moves[selected_moves[0]]
        # This works because the index into the list of all_possible_moves
        # matches up with the index of the key (board as a 2 dimensional tuple) of 
        # the dictionary all_possible_win_draw_probabilities.
                
        return selected_move

