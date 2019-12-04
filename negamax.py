from player import Player
from tic_tac_toe import TicTacToe

class NegaMax(Player, TicTacToe):
    """This is the User Inteface that allows a user to play the game."""
    
    def __init__(self, depth=2):
        super().__init__()
        self.depth = depth
            
    def get_move(self, board, possible_moves, player_1_or_2):
        """Given the current board layout, a list of possible moves, 
        and the current player (1 or 2 =  -1)
        this will return one move from the list.
        
        It will return the index of the move in the list 
        of possible moves passed in.
        
        """
        
        print('Current board: ')
        print(board)
        
        print('possible_moves:', possible_moves)
        
        print('Current player 1 or 2 (-1):', player_1_or_2)
                
        win_loss, best_move, game_over = self.negamax(board, player_1_or_2, self.depth) 
            
        move_tuple = best_move
        
        print('The negamax method just returned - move_tuple:', move_tuple)
        
        move_index = possible_moves.index(move_tuple)
        print ('move_index:', move_index)
        
        print('int(move_index):', int(move_index))
        print()
        return int(move_index)
        
    
    def negamax(self, board, player_1_or_2, depth):
        # Given a Tic-Tac-Toe 3x3 board position where 1 => current player's square,
        # -1 => opponent's square, 0 => blank square,
        # this will return the current player's best move as the x and y indexes into 
        # the board array.
        # The second input parameter, player_1_or_2, is 1 or -1 to indicate which player's
        # move it is.

        best_move = ()

                
        # Attempt to fix bug in NegaMax game playing - may need to account for player 1 vs 2.
        # This bypasses the caching in get_board_result above. Using it now for test purposes.
        game_over, win_loss = self.check_win_loss_draw_for_either_player(board, player_1_or_2)


        if game_over:

            # only when returning to original caller, do we need the best move. Here we
            # return for test purposes, for example, testing by passing in a full board.
            # Similarly only the original caller cares about whether game_over is 
            # true, i.e. whether the game is over "now", as opposed to two or more moves
            # down the tree.
            return win_loss, best_move, game_over 
            # As the tree descent only ends when the game is over
            # a zero returned back up the tree indicates a draw.
            # As only the root node needs to return the best_move, and the method
            # should never be called with a board position where the game is over
            # (i.e. we can't determine the best move if the game is over) it is 
            # not necessary to return the best move here.

        if depth == 0: # The depth of the search is limited to constrain search time etc
            return win_loss, best_move, game_over

        win_loss = -2 # initialize to less than worst possible value = a loss, 
        # so that even if all moves result in a loss, it will still pick a move
        # i.e. we will use Max later to determine the next move.
        
        for i,j in self.get_all_possible_moves(board):
            # Use i,j below to reset the board by setting this back to zero 
            # after we have determined which move is best
            # Update the board with each possible move to determine which is best
            board[i,j] = player_1_or_2 # 1 or -1, depending on who's move it is

            # we negate the player value, as the players alternate taking moves.
            # We negate negamax because what is good for one player is bad for the other.
            win_loss_result, _, _ = self.negamax(board, -player_1_or_2, depth-1)

            # We don't use the best_move returned by negamax here
            # only when returning to original caller, do we need the best move

            # [Similarly we don't care about game_over here either, as that is only
            # relevant if the game is over "now", as opposed to two or more moves down the
            # road.]

            win_loss_new = max(win_loss, -win_loss_result)

            board[i,j] = 0 # reset the board to the way it was, before this move
            # i.e. undo this move

            if win_loss_new > win_loss: # then we chose this move as best for this player
                best_move = (i,j)
                win_loss = win_loss_new


        # only when returning to original caller, do we need the best move
        return win_loss, best_move, game_over
