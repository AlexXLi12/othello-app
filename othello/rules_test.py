import pytest
from .rules import *


@pytest.fixture
def starting_board():
    return ['.'] * 27 + ['O', 'X'] + ['.'] * 6 + ['X', 'O'] + ['.'] * 27


@pytest.fixture
def midgame_board():
    return ['.'] * 27 + ['O', 'O', 'O'] + ['.'] * 5 + \
        ['X', 'O', 'O'] + ['.'] * 4 + ['X', 'O', 'O', 'O'] + ['.'] * 18


def test_check_move_starting(starting_board):
    assert check_move(starting_board, 26, 27, 'X') == 28
    assert check_move(starting_board, 19, 27, 'X') == 35
    assert check_move(starting_board, 26, 19, 'O') == -1


def test_check_move_midgame(midgame_board):
    assert check_move(midgame_board, 19, 27, 'X') == 35
    assert check_move(midgame_board, 34, 35, 'O') == 36
    assert check_move(midgame_board, 26, 27, 'X') == -1
    assert check_move(midgame_board, 26, 19, 'O') == -1


def test_possible_moves_starting(starting_board):
    assert get_possible_moves(starting_board, 'X') == {19, 26, 37, 44}
    assert get_possible_moves(starting_board, 'O') == {20, 29, 34, 43}


def test_possible_moves_midgame(midgame_board):
    assert get_possible_moves(midgame_board, 'X') == {38, 46, 51, 19, 21, 53}
    assert get_possible_moves(midgame_board, 'O') == {26, 34, 41, 49}


def test_update_board_starting(starting_board):
    board = update_board(starting_board, 'X', 26)
    assert board == ['.'] * 26 + ['X', 'X', 'X'] + \
        ['.'] * 6 + ['X', 'O'] + ['.'] * 27
    # Invalid move, board should not change
    board = update_board(board, 'O', 19)
    assert board == ['.'] * 26 + ['X', 'X', 'X'] + \
        ['.'] * 6 + ['X', 'O'] + ['.'] * 27


def test_update_board_midgame(midgame_board):
    board = update_board(midgame_board, 'X', 19)
    assert board == ['.'] * 19 + ['X'] + ['.'] * 7 + ['X', 'O', 'O'] + ['.'] * \
        5 + ['X', 'O', 'O'] + ['.'] * 4 + ['X', 'O', 'O', 'O'] + ['.'] * 18
    board = update_board(board, 'O', 34)
    assert board == ['.'] * 19 + ['X'] + ['.'] * 7 + ['X', 'O', 'O'] + ['.'] * \
        4 + ['O', 'O', 'O', 'O'] + ['.'] * 4 + \
            ['X', 'O', 'O', 'O'] + ['.'] * 18
