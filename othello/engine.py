from .constants import *
from .classes import Square
import time
moveBoards = {}
LIMIT_AB = 6
def sortMoves(possibles):
    cnrs = [*possibles & corners]
    asqrs = [*possibles & asquares]
    rest = possibles - corners
    return [*cnrs, *asqrs, *rest]

def calcMove(board:list[Square], player:int):
    """Return the index of the engine's move

    Args:
        board (list[Square]): _description_
        player (int): int which specifies whose turn it is (-1 == black, 1 == white)
    """
    board = ''.join(['X' if square.player == -1 else 'O' if square.player == 1 else '.'for square in board])
    token = 'X' if player == -1 else 'O'
    #board is filled
    if '.' not in board:
        return -1
    startTime = time.time()
    #default depth 6
    return alphabeta(board, token, float("-inf"), float("inf"), LIMIT_AB, startTime, 2)[1]


def calc_move(board: list[str], to_move: str, depth_limit: int = LIMIT_AB, time_limit: float = 2):
    """Return the index of the engine's move

    Args:
        board (list[str]): list of strings representing the board
        to_move (str): str which specifies whose turn it is ('X' == black, 'O' == white)
    """
    # board is filled
    if '.' not in board:
        return -1
    board = "".join(board)
    startTime = time.time()
    # default depth 6
    # iterative deepening
    current_depth = 0
    while time.time() - startTime < time_limit:
        current_depth += 1
        move = alphabeta(board, to_move, float("-inf"), float("inf"), depth_limit, startTime, time_limit)[1]
    return move

def alphabeta(board, token, alpha, beta, depth, startTime, timeLimit):
    global seenBoards
    eToken = "XO"[token == "X"]
    if "." not in board:
        return (1000 * (board.count(token) - board.count(eToken)), None)
    possibles = possibleMoves(board, token)
    if not possibles:
        if not possibleMoves(board, eToken):
            # end game
            return (1000 * (board.count(token) - board.count(eToken)), None)
        if depth != 0:
            # pass turn
            nm = alphabeta(board, eToken, -beta, -alpha, depth, startTime, timeLimit)
            seenBoards[(board, token)] = -nm[0]
            return (-nm[0], -1)
    if depth == 0:
        # depth limit reached
        # calculate score and return
        score = calculateBoardScore(board, token)
        seenBoards[(board, token)] = score
        return (score, None)
    maxTuple = (float("-inf"), ())
    psbls_sorted = sortMoves(possibles)
    # looping through moves
    for move in psbls_sorted:
        newBoard = makeMove(move, board, token)
        if (newBoard, token) in seenBoards:
            score = seenBoards[(newBoard, token)]
            if score <= maxTuple[0]:  # if board score <= current max, ignore and continue
                continue
            if score > maxTuple[0]:
                maxTuple = (score, move)
        else:
            nm = alphabeta(newBoard, eToken, -beta, -alpha, depth - 1, startTime, timeLimit)
            if -nm[0] > maxTuple[0]:
                maxTuple = (-nm[0], move)
                alpha = max(alpha, maxTuple[0])
            seenBoards[(newBoard, token)] = -nm[0]
        if alpha > beta:
            break
    return maxTuple

seenBoards = dict()
def calculateBoardScore(board, token):
    # evaluates based on csquares, xsquares, asquares, bsquares, corners, and center4
    eToken = "XO"[token == "X"]
    total = 0
    # calculate stable disks score
    for idx in corners:
        if board[idx] == token:
            for diff in cornerDirections[idx]:
                nextIdx = idx + diff
                while nextIdx >= 0 and nextIdx <= 63 and board[nextIdx] == token:
                    total += 10  # stable
                    nextIdx += diff
        elif board[idx] == eToken:
            for diff in cornerDirections[idx]:
                nextIdx = idx + diff
                while nextIdx >= 0 and nextIdx <= 63 and board[nextIdx] == eToken:
                    total -= 10  # stable
                    nextIdx += diff
    for idx in csquares:
        if board[idx] == token and board[cxsquaresToCorner[idx]] == ".":
            total -= 75
        if board[idx] == eToken and board[cxsquaresToCorner[idx]] == ".":
            total += 75
    for idx in xsquares:
        if board[idx] == token and board[cxsquaresToCorner[idx]] == ".":
            total -= 75
        if board[idx] == eToken and board[cxsquaresToCorner[idx]] == ".":
            total += 75
    for idx in asquares:
        if board[idx] == token:
            if board[asquarePairs[idx]] == token:
                total += 12
            total += 12
        elif board[idx] == eToken:
            if board[asquarePairs[idx]] == eToken:
                total -= 12
            total -= 12
    for idx in bsquares:
        if board[idx] == token:
            total += 2
        elif board[idx] == eToken:
            total -= 2
    for idx in corners:
        if board[idx] == token:
            total += 200
        elif board[idx] == eToken:
            total -= 200
    for idx in center4:
        if board[idx] == token:
            total += 3
        elif board[idx] == eToken:
            total -= 3
    return total + len(removeBad(possibleMoves(board, token), board, token)) * 10

def makeMove(moveIdx, board, toMove):
    if (moveIdx, board, toMove) in moveBoards:
        return moveBoards[(moveIdx, board, toMove)]
    lst = list(board)
    opposite = "XO"[toMove == "X"]
    for nbrIdx in neighbors[moveIdx]:
        if board[nbrIdx] == opposite:
            for k in range(len(rays[moveIdx])):
                diff = rays[moveIdx][k]
                nextIdx = moveIdx + diff
                while board[nextIdx] == opposite and nextIdx != bounds[moveIdx][k]:
                    nextIdx += diff
                if board[nextIdx] == toMove and nextIdx != moveIdx + diff:
                    for i in range(moveIdx, nextIdx, diff):
                        lst[i] = toMove
    moveBoards[(moveIdx, board, toMove)] = "".join(lst)
    return "".join(lst)

seenpsbls = {}
def possibleMoves(board, toMove):
    global seenpsbls
    if (board, toMove) in seenpsbls:
        return seenpsbls[(board, toMove)]
    opposite = "XO"[toMove == "X"]
    if board.count(toMove) < board.count("."):
        target = "."
        other = toMove
    else:
        other = "."
        target = toMove
    possibleMoves = set()
    for pos in range(64):
        if board[pos] != other:
            continue
        for k in range(len(rays[pos])):
            diff = rays[pos][k]
            nextIdx = pos + diff
            while board[nextIdx] == opposite and nextIdx != bounds[pos][k]:
                nextIdx += diff
            if board[nextIdx] == target and nextIdx != pos + diff:
                if target == ".":
                    possibleMoves.add(nextIdx)
                else:
                    possibleMoves.add(pos)
    seenpsbls[(board, toMove)] = possibleMoves
    return possibleMoves

def removeBad(moves, board, token):
    moves = list(moves)
    for move in moves:
        if move in cxsquaresToCorner and board[cxsquaresToCorner[move]] != token:
            moves.pop(moves.index(move))
    return set(moves)