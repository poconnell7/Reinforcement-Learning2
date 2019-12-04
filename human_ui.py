from player import Player

class HumanUI(Player):
    """This is the User Inteface that allows a user to play the game."""
    
    def get_move(self, board, possible_moves, player_1_or_2):
        """Given the current board layout, a list of possible moves, 
        and the current player (1 or 2 =  -1)
        this will return one move from the list.
        
        It will return the index of the move in the list 
        of possible moves passed in.
        
        """

        print('UI ~ Current player 1 or 2(= -1):', player_1_or_2)
        
        print('UI ~ Current board : ')
        print(board)
        
        print('UI ~ possible_moves:', possible_moves)
        
        # input will return the user entered values as a string
        move_index = input("""
        UI ~ Please enter the zero-based index of the desired move from the list of possible moves:\n\n """)
        
        print ('UI ~ HumanUI: move_index:', move_index)

        print('UI ~ int(move_index):', int(move_index))
        print()
        return int(move_index)
        