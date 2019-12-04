import numpy as np
from tic_tac_toe import TicTacToe
from board_position_states import BoardPositionStates

class ReinforcementLearning(TicTacToe):
    """The following class exposes a method that calculates the best move 
    for the current player given the current board position. 
    It also keeps track of each new game position the best move led to, 
    so it can update the win/draw probabilities at the end of game 
    for each of these positions.
    
    For Player 2 the value of -1 must be passed into the init method (not the number 2).
    
    This keeps track of each move played by the Reinforcement algorithm 
    and updates the win probabilites at the end of the game 
    for each board position."""
        
    # An instance of this class is created for each game.
    # The player can't be changed once the game (/training) has started.
    # The internal Board Position States are dependent on which player is which
    # i.e. the probability of winning from a given position depends on which player you are.
    # We would have to invert all the board keys in the dictionary if we allowed changing players.
    def __init__(self, player_1_or_2):
        self.list_board_positions_moved_to = [] # keep track of positions for one game
        self.current_player = player_1_or_2 # player (1 or -1); fixed for all games
        self.win_draw_loss_record = [] # Keep track of results across multiple games
        
        self.board_position_states = BoardPositionStates() # This should track
        # the win probability for each position across multiple games.
        
    def update_probabilities_as_game_is_over(self, final_result):
        # The parameter final_result is either 1, 0, or -1, corresponding
        # a win, draw, or a loss.
        # The final_result should have been inverted already if this is player 2 (= -1)
        
        self.win_draw_loss_record.append(final_result)
        
        number_board_position_states_to_update = len(self.list_board_positions_moved_to)
                
        # Default to neither win nor draw, and then only update as necessary
        current_win_outcome = 0
        current_draw_outcome = 0
        
        if final_result == 1: # We won this game
            
            current_win_outcome = 1 # 100% chance of winning
            #current_draw_outcome = 0 # => 0% chance of drawing
            
            last_position_moved_to = self.list_board_positions_moved_to[-1]
            
            last_state = self.board_position_states.get_state(last_position_moved_to)
            
            last_state.update_probabilities_after_win()
            number_board_position_states_to_update -= 1 # Decrement by one i.e. we just
            # updated the last position that we moved to.
                        
        elif final_result == 0: # This game was a draw           
            #current_win_outcome = 0
            current_draw_outcome = 1
            
        #else final_result = -1 so both are zero = default set above
            
        # If final_result is 1 (win) we will first update the second last
        # position here by passing in 1, which is also the value in the last position, 
        # which was set to 1 just above.
        # Otherwise we will first be setting the final position, using the final
        # result.
          
        # we need to go through this, in reverse order, from the end of the list 
        # i.e. the last one updates the second last one, and the second
        # last one updates the third last one, and so on.
        reversed_number_board_position_states_to_update = \
            reversed(np.arange(number_board_position_states_to_update))
        
            
        for index in reversed_number_board_position_states_to_update:
            
            current_board_position_moved_to = self.list_board_positions_moved_to[index]

            current_state = \
                    self.board_position_states.get_state(current_board_position_moved_to)

            
            current_state.update_win_probability_based_on_next_outcome(\
                                                                current_win_outcome)
            
            current_state.update_draw_probability_based_on_next_outcome(\
                                                                current_draw_outcome)
            
            # Now use the updated win and draw probabilities for the current
            # board position to update the next board position states 
            current_win_outcome = current_state.get_win_probability()
            current_draw_outcome = current_state.get_draw_probability()
            
        # Clear the list of board positions used during this game,
        # in preparation for the next game.
        self.list_board_positions_moved_to = []
            
    
    def get_move(self, board, possible_moves, player_1_or_2):
        """Given the current board layout, a list of possible moves, 
        and the current player (1 or 2 =  -1)
        this will return one move from the list.
        
        It will return the index of the move in the list 
        of possible moves passed in.
        
        """

        # Given a Tic-Tac-Toe 3x3 board position where 1 => current player's square,
        # -1 => opponent's square, 0 => blank square,
        # this will return the current player's best move [as the x and y indexes into 
        # the board array.]
        # The second input parameter, player_1_or_2, is 1 or -1 to indicate which player's
        # move it is. 
    
        print('RL ~ Current player 1 or 2 (= -1):', player_1_or_2)
        
        print('RL ~ Current board: ')
        print(board)
        
        print('RL ~ possible_moves:', possible_moves)

        next_move = () 

        # This will be the best move i.e. the move with the current
        # value of highest winning probability except when it is making exploratory
        # (as opposed to greedy) moves.

        next_move = self.board_position_states.get_next_move(board, possible_moves, self.current_player)

        next_move_location_tuple = possible_moves[next_move]
        board[next_move_location_tuple] = self.current_player

        self.list_board_positions_moved_to.append(board.copy()) # This board that we are
        # appending here could be changed by the next line of code, for example.
        # Hence we need to make a copy

        board[next_move_location_tuple] = 0 # undo the move in case it affects the calling method.

        return next_move

