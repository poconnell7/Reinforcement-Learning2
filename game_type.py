class GameType:
    """Initially this would be used for Tic-Tac-Toe, but could also be used for Connect4 in the future.
    
    Hence it is defined here as a base class without implementation (except the init function), 
    sort of an interface definition.
    """
    
    def __init__(self):
        self.position_results_dictionary = {}
    
    def get_board_after_move(self, current_board, new_move):
        """Returns the new board resulting from 'playing' the move on the current board"""
        
    def get_all_possible_moves(self, board):
        """Given a board position this will return all possible moves"""
               
    def get_board_result(self, board):
        """Returns the result of the current board state.
        
        This returns True or False to indicate if the game is over or not.
        
        If the game is over, then this returns 1, 0, or -1.
        The return value of 1 means the player represented by 1 on the board is the winner.
        Returning -1 means the player whose moves are represented by -1 on the board won.
        Zero would mean a draw.
        """
        
    def two_dim_array_to_tuple(self, two_dim_array):
        """Converts a two dimensional array to a tuple so it can be used a key in a dictionary
        i.e. dictionary keys must be immutable (to be hashable!?)
        """
        
        return tuple(tuple(i for i in vector) for vector in two_dim_array)  
               
#     def invert_board(self, board):
#         """This returns the board passed in except with 1 and -1 interchanged.
        
#         This would be used if we wanted to switch the board positions, 
#         depending on which player it was being used for.
#         However it may not be needed, so this is just a placeholder for now.
#       """