from .classes import Square
from .constants import *

def possibleMoves(board:list, player:int):
    """Return the list of indices of possible moves for the player specified.

    Args:
        board (list[Square]): list of Square objects representing the Othello board
        player (int): int which specifies whose turn it is (-1 == black, 1 == white)

    Returns:
        list(int): list of integers representing indices on the game board
    """
    opposite = player*-1
    tokens = [index for index, square in enumerate(board) if square.player == player] #get index of all positions of piece to move
    toCheck = [] # (idx of player, idx of opposing neighbor)
    possibleMoves = set()
    for pos in tokens:
        for nbrIdx in neighbors[pos]:
            if board[nbrIdx].player == opposite:
                toCheck.append([pos,nbrIdx])
    for idx, nbrIdx in toCheck:
        diff = nbrIdx-idx
        nextIdx = idx+diff
        while nextIdx >=0 and nextIdx <= 63:
            if abs(diff) != 8 and (nextIdx%8 == 7 or nextIdx%8 == 0):
                if board[nextIdx].player == player: break
                if board[nextIdx].player == 0: 
                    possibleMoves.add(nextIdx)
                break
            if board[nextIdx].player == player: break
            if board[nextIdx].player == 0: 
                possibleMoves.add(nextIdx)
                break
            nextIdx += diff
    return possibleMoves 

def updateBoard(board:list, player:int, move:int):
    """Play the move on the board, flipping appropriate tiles

    Args:
        board (list[Square]): list of Square objects representing the Othello board
        player (int): int which specifies whose turn it is (-1 == black, 1 == white)
        move (int): index of move
    """
    opposite = player*-1
    toCheck = [] # (list of indices of enemy tokens around move)
    for idx in neighbors[move]:
        if board[idx].player == opposite:
            toCheck.append(idx)
    for nbrIdx in toCheck:
        if (nextMove:=checkMove(board,move,nbrIdx, player)) >= 0:
            big = max(move, nextMove)
            small = min(move, nextMove)
            for i in range(small, big+1, abs(move-nbrIdx)):
                board[i].placePiece(player)
    return board

def checkMove(board, idx, nbrIdx, target):
    """Check if move is valid

    Args:
        board (list[Square]): list of Square objects representing the Othello board
        idx (int): index of origin piece
        nbrIdx (int): index of opposing player's neighboring tile
        target (int): int which specifies whose turn it is (-1 == black, 1 == white)

    Returns:
        int: final index at which piece can be placed
    """
    ignore = board[nbrIdx].player
    token = board[idx].player
    diff = nbrIdx - idx
    nextIdx = nbrIdx
    if abs(diff) == 8: #vertical case
        while nextIdx >= 0 and nextIdx <= 63:
            if board[nextIdx].player == target:
                return nextIdx
            if board[nextIdx].player != ignore:
                return -1
            nextIdx += diff
    else: #horizontal and diagonal case
        while nextIdx >= 0 and nextIdx <= 63:
            if board[nextIdx].player == target:
                return nextIdx
            if board[nextIdx].player != ignore:
                return -1 
            if (nextIdx%8 == 7 or nextIdx%8 == 0):
                return -1
            nextIdx += diff
    return -1

def get_possible_moves(board:list, to_move:str):
    """Return the list of indices of possible moves for the player specified.

    Args:
        board (list[str]): list of strings representing the Othello board
        to_move (str): string which specifies whose turn it is ('X' == black, 'O' == white)

    Returns:
        list(int): list of integers representing indices on the game board
    """
    # get index of all positions of piece to move
    opposite = 'O' if to_move == 'X' else 'X'
    tokens = [index for index, square in enumerate(
        board) if square == to_move]
    toCheck = []  # (idx of player, idx of opposing neighbor)
    possibleMoves = set()
    for pos in tokens:
        for nbrIdx in neighbors[pos]:
            if board[nbrIdx] == opposite:
                toCheck.append([pos, nbrIdx])
    for idx, nbrIdx in toCheck:
        diff = nbrIdx-idx
        nextIdx = idx+diff
        while nextIdx >= 0 and nextIdx <= 63:
            if abs(diff) != 8 and (nextIdx % 8 == 7 or nextIdx % 8 == 0):
                if board[nextIdx] == to_move:
                    break
                if board[nextIdx] == '.':
                    possibleMoves.add(nextIdx)
                break
            if board[nextIdx] == to_move:
                break
            if board[nextIdx] == '.':
                possibleMoves.add(nextIdx)
                break
            nextIdx += diff
    return possibleMoves

def update_board(board:list, to_move:str, move:int):
    """Update the board with the move specified. Assumes move is valid.

    Args:
        board (list): represents the Othello board. '.' for empty, 'X' for black, 'O' for white
        to_move (str): 'X' for black, 'O' for white
        move (int): index of the move to make
    """
    opposite = 'O' if to_move == 'X' else 'X'
    toCheck = []  # (list of indices of enemy tokens around move)
    for idx in neighbors[move]:
        if board[idx] == opposite:
            toCheck.append(idx)
    for nbrIdx in toCheck:
        if (nextMove := check_move(board, move, nbrIdx, to_move)) >= 0:
            big = max(move, nextMove)
            small = min(move, nextMove)
            for i in range(small, big+1, abs(move-nbrIdx)):
                board[i] = to_move
    return board

def check_move(board, idx, nbrIdx, target):
    """Check if move is valid

    Args:
        board (list[str]): list of strings representing the Othello board
        idx (int): index of origin piece
        nbrIdx (int): index of opposing player's neighboring tile
        target (str): 'X' for black, 'O' for white

    Returns:
        int: final index at which piece can be placed
    """
    ignore = 'O' if target == 'X' else 'X'
    diff = nbrIdx - idx
    nextIdx = nbrIdx
    if abs(diff) == 8:  # vertical case
        while nextIdx >= 0 and nextIdx <= 63:
            if board[nextIdx] == target:
                return nextIdx
            if board[nextIdx] != ignore:
                return -1
            nextIdx += diff
    else:  # horizontal and diagonal case
        while nextIdx >= 0 and nextIdx <= 63:
            if board[nextIdx] == target:
                return nextIdx
            if board[nextIdx] != ignore:
                return -1
            if nextIdx % 8 == 7 or nextIdx % 8 == 0:
                return -1
            nextIdx += diff
    return -1