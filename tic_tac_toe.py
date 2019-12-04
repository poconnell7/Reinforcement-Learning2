import numpy as np
from game_type import GameType

class TicTacToe(GameType):
    """Contains the functionality needed for the game of Tic-Tac-Toe.
    
    This class caches the win/draw/loss result, if any, for each board position 
    to improve performance by avoiding having to calculate the result 
    of a given board position more than once.
    
    This class will probably not be instantiated as is, (except for test purposes),
    but rather will be a inherited by other classes.
    """
    
    def __init__(self):
        super().__init__()
    
    def get_board_after_move(self, current_board, new_move):
        """Returns the new board resulting from 'playing' the move on the current board.
        
        The new_move is in the form of a nested tuple, with the player, 1 or -1 first.
        For example (-1, (0,0))
        The second part of the tuple is the location of the move, in the form of another tuple.
        The first element indicates the row, the second the column. Both are zero based.
        """
        
        print("Original 'new' move:", new_move)
        
        board = current_board.copy()
        player_move_indicator = new_move[0]
        if player_move_indicator not in (1,-1):
            raise ValueError('Only 1 or -1 are valid values for the player')

        # Update the board with the new move
        move_location = new_move[1]
        if  board[move_location] == 0: # this space on the board is currently empty
            board[move_location] = player_move_indicator
        else: # This space on the board is already occupied
            raise ValueError(f'''Invalid move {new_move} for player {player_move_indicator}. 
            This space {move_location} on the board
            
            {board}
            
            is already taken by {board[move_location]}''')
            
        return board

        
    def get_all_possible_moves(self, board):
        """Given a Tic-Tac-Toe 3x3 board position where 
        1 => Player 1,
        -1 => Player 2, 
        0 => blank square,
        this will return all possible moves (i.e. blank squares) as a list of x,y tuples
        """
        
#       this will return all possible moves as a list of integers from 1 to 9, 
#         representing the 9 squares on the board. 
    
        possible_moves = []

        board_width = board.shape[0]
        board_height = board.shape[1]

        for i in range(board_width):
            for j in range(board_height):
                if board[i,j] == 0: # add this empty square to the list of possible moves
                    possible_moves.append((i,j))
                    # just use tuples for TTT moves. Worry about C4 when we get there
                    #possible_moves.append(convert_move_tuple_to_one_based_integer(i,j))               

        return possible_moves
    
    
    def get_board_result(self, board):
        """Returns the result of the current board state.
        
        This returns True or False to indicate if the game is over or not.
        
        If the game is over, then this returns 1, 0, or -1.
        The return value of 1 means the player represented by 1 on the board is the winner.
        Returning -1 means the player whose moves are represented by -1 on the board won.
        Zero would mean a draw.
        """
        
        board_key = self.two_dim_array_to_tuple(board) # np arrays are not hashable
        # So convert two dimensional array to two dimensional tuple, 
        # so it can be used as a key in dictionary.
                
        if board_key in self.position_results_dictionary:
            game_over, win_loss = self.position_results_dictionary[board_key]
        else: # Get/calculate board position results
            game_over, win_loss = self.check_win_loss_draw(board)

            # Store it in a dictionary
            self.position_results_dictionary[board_key] = game_over, win_loss
            
        return game_over, win_loss
    
    
    def get_win_loss(self, sum_3_squares):
        """Given the sum of three squares on the board this returns a 1, -1, or 0
        indicating a win for player 1, a win for player -1, or neither (0).
        """
        if sum_3_squares == 3:
            return 1 # player 1 won
        if sum_3_squares == -3:
            return -1 # player 1 lost (player -1 won)
        return 0 # [else] these three squares do not all belong to the same player
        
    # This is currently only used by NegaMax 
    # [And temporarily the reinforcment learning algorithm]
    # i.e. other uses are OK with always getting result
    # from point of view of Player1. If NegaMax uses this directly it will bypass the caching
    # in get_board_result above. Try it now for test purposes to see if it fixes the bug.
    def check_win_loss_draw_for_either_player(self, board, player_1_or_2):
        # This checks the win/loss/draw status from the point of view of the player (1 or -1)
        # passed in as parameter 2. It does this by simply multiplying player_1_or_2 by the 
        # win/draw/loss result (1/0/-1) for player 1.

        # Check win/loss/draw from point of view of Player1 = 1
        game_over, win_loss_for_p1 = self.check_win_loss_draw(board)
        
        # Adjust win/loss depending on who the current player is 
        win_loss = player_1_or_2 * win_loss_for_p1 
        
        return game_over, win_loss,  

 
    def check_win_loss_draw(self, board):
        """ The input parameter board is a 3x3 matrix, [numpy array]
        which represents the current board position
        Each cell contains 3 possible values 1, 0, or -1
        1 means it "belongs" to the player 1
        0 means it is empty
        -1 means it was taken by the player 1's opponent

        The method will return an integer, indicating a win(1) or a loss(-1) for player 1
        , and also a boolean indicating if the game is over.

        Any 3 marks in a row is considered a win: horizontal, vertical or diagonal
        If the board is full (i.e. no more cells with zero), then there are no 
        more possible moves. In this situation, if neither side has won, then it is a draw.

        If the sum of any three boxes in a row is 3 => the current player (1) has won.
        In this case the method will return a 1
        If the sum of any three boxes in a row is -3, the current player has lost.
        In this case the method will return -1 
        We assume the game stops once one player wins, so there should never
        be two rows, one adding up to 3, and another adding up to -3.
        If the game is a neither won nor lost, we will return zero.
        If we return zero, the game may or may not be over.
        However, in this case the boolean return value indicates if the game is over or not.
        """

        game_over = False
        win_loss = 0 # defaults to neither win nor loss
        board_full = True # default to  board full, 
        # and reset after finding first blank square

        board_width = board.shape[0]
        board_height = board.shape[1]

        row_sums = np.zeros(board_width, dtype=int)
        column_sums = np.zeros(board_height, dtype=int)

        # First entry in diagonal_sums will be where X=Y
        # Second entry will be for other diagonal, where X+Y=2
        diagonal_sums = np.zeros(2, dtype=int) # This works for tic-tac-toe 
        # but for Connnect 4 there would be more scenarios.

        for i in range(board_width):
            for j in range(board_height):

                # If any square is blank the board is not full
                if board[i,j] == 0:
                    board_full = False

                # Every square on the board belongs to both a row and a column
                row_sums[i] += board[i,j]
                column_sums[j] += board[i,j]

                # We can identify if the cell is on a diagonal from the two index values
                if i==j: # diagonal from top left to bottom right
                    diagonal_sums[0]+=board[i,j]

                # diagonal from top right to bottom left
                #if i+j==2: # this works for a 3x3 matrix
                if i+j==board_width-1:                 
                    diagonal_sums[1]+=board[i,j]
                    # this will work for any square matrix!? => useful for testing.

                # One cell, the middle one, is added to both diagonals

        for i in range(board_width):
            if win_loss != 0: # A win or a loss has already been recorded
                break
            win_loss = self.get_win_loss(row_sums[i])

        for j in range(board_height):
            if win_loss != 0: # A win or a loss has already been recorded
                break
            win_loss = self.get_win_loss(column_sums[j])

        for d in range(2):
            if win_loss != 0: # A win or a loss has already been recorded
                break
            win_loss = self.get_win_loss(diagonal_sums[d])

        # The game is over if one player won or if the board is full
        if win_loss != 0 or board_full:
            game_over = True

        #return (win_loss*player_1_or_2), game_over
#         return win_loss, game_over
        return game_over, win_loss, 

    # if True and 0 is returned, it means the game is over and it is a draw
