import numpy as np
from tic_tac_toe import TicTacToe
from human_ui import HumanUI

class Game(TicTacToe):
    """Represents a game of Tic-Tac-Toe.
    
    Manages two players, indicated by their game board markers 1 (player 1), and -1 (player 2).
    Keeps track of the current board position, each player's moves, and the final outcome.
    """
    
    def __init__(self):
        super().__init__()
        # Player 1 always goes first.
        # Player 2 has the -1 game board marker.
        # Initialize the empty board
        self.board = np.zeros((3,3), dtype=int) 
        
    def start(self, player1, player2):
        game_over = False
        players = (player1, player2)
        
        # Player 1 will go first, but set everything to Player 2 here 
        # because it is updated at the beginning of the While loop
        player_move_indicator = -1       
        current_player_index = 1 # zero based
        
        while not game_over:            
            # Change players at the start of every iteration through the loop
            player_move_indicator *= -1
            
            current_player_index = (current_player_index + 1) % 2
           
            current_player = players[current_player_index]
            
            # Handle errors by the user i.e. Human UI not the algorithms 
            # (i.e. just printing errors for the latter would probably result in infinite loops.)
            try:

                possible_moves = self.get_all_possible_moves(self.board)

                # Add error handling here so game doesn't terminate if user makes a mistake
                # but throw exception for algorithms - to avoid infinite loops.
                # Could also put this error handling in UI i.e. only for user (but what about move that is already taken).
                # We check type of player object passed in and only catch error if it is a UI.

                move_index = current_player.get_move(self.board, possible_moves, player_move_indicator)
                move_location = possible_moves[move_index]

                move = (player_move_indicator, move_location)

                self.board = self.get_board_after_move(self.board, move)

                game_over, win_loss = self.get_board_result(self.board)
                
                print()
                print(f'game_over: {game_over}; win_loss: {win_loss}')  
                print()
            
            except Exception as err:
                if isinstance(current_player, HumanUI): 
                    # Don't exit in the middle of a game because the user entered an invalid index
                    # for the possible moves list. For algorithm we throw the error to avoid infinite loops
                    print('\nProbable user entry error:', repr(err), '\nPlease try again\n')
                    
                    # Compensate for the player changing incorrectly at the beginning of the loop 
                    # by changing it now (too) i.e. the error means this player should go again
                    player_move_indicator *= -1
                    current_player_index = (current_player_index + 1) % 2
                    current_player = players[current_player_index]
                else: # error occurred on algorithm's move so exit to avoid possible infinite loop
                    raise # re-raise the exception
                        
        print('Game is over. Final Board position:')
        print(self.board)
        player1.update_probabilities_as_game_is_over(win_loss)
        player2.update_probabilities_as_game_is_over(-1 * win_loss) # invert result so it is correct for player 2(= -1)
