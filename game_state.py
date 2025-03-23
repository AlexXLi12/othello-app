import othello.rules

class GameState:
    """
    Represents the game state of an Othello game.
    """
    def __init__(self):
        self.board = ['.'] * 27 + ['O', 'X'] + ['.'] * 6 + ['X', 'O'] + ['.'] * 27
        self.to_move = 'X' # X = black, O = white
        self.possible_moves = othello.rules.get_possible_moves(self.board, self.to_move)
        self.move_history = []
        self.winner = None
    
    def __str__(self):
        return self.board
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.board == other.board
    
    def make_move(self, move):
        """Make a move on the board.

        Parameters:
            move (int): The index of the move to make.
        
        Returns:
            bool: True if the move was valid and made, False otherwise.
        """
        # check if move is valid
        if move not in self.possible_moves:
            return False
        # move is valid; update game state
        self.board = othello.rules.update_board(self.board, self.to_move, move)
        self.move_history.append(move)
        self.to_move = 'X' if self.to_move == 'O' else 'O'
        self.possible_moves = othello.rules.get_possible_moves(self.board, self.to_move)
        return True