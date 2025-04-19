import pytest
from .rules import *

@pytest.fixture
def starting_board():
    return ['.'] * 27 + ['O', 'X'] + ['.'] * 6 + ['X', 'O'] + ['.'] * 27

@pytest.fixture
def midgame_board():
    return ['.'] * 27 + ['O', 'O', 'O'] + ['.'] * 5 + ['X', 'O', 'O'] + ['.'] * 4 + ['X', 'O', 'O', 'O'] + ['.'] * 18

def test_check_move_starting(starting_board):
    assert check_move(starting_board, 26, 27, 'X') == 28
    assert check_move(starting_board, 19, 27, 'X') == 35 

# TODO: Fix these tests
#def test_check_move_midgame(midgame_board):
    #assert check_move(midgame_board, 26, 27, 'X') == 28
    #assert check_move(midgame_board, 19, 27, 'X') == 35 

def test_possible_moves_midgame(midgame_board):
    assert get_possible_moves(midgame_board, 'X') == {38, 46, 51, 19, 21, 53}