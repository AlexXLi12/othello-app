from .constants import *
import time
moveBoards: dict[tuple[int, str, str], str] = {}
LIMIT_AB = 6
def sortMoves(possibles: set[int]):
    cnrs = [*possibles & corners]
    asqrs = [*possibles & asquares]
    rest = possibles - corners
    return [*cnrs, *asqrs, *rest]

def calc_move(board: list[str], to_move: str, depth_limit: int = LIMIT_AB, time_limit: float = 2):
    """Return the index of the engine's move

    Args:
        board (list[str]): list of strings representing the board
        to_move (str): str which specifies whose turn it is ('X' == black, 'O' == white)
    """
    global seenBoards
    # board is filled
    if '.' not in board:
        return -1
    board_str = "".join(board)
    startTime = time.time()
    # default depth 6
    # iterative deepening
    current_depth = 0
    best_score, best_move = float("-inf"), -1
    while time.time() - startTime < time_limit and current_depth < depth_limit:
        seenBoards: dict[tuple[str, str], float|int] = dict()
        current_depth += 1
        score, move = alphabeta(board_str, to_move, float("-inf"), float("inf"), current_depth, startTime, time_limit)
        if move == -2:
            print('Time limit reached')
            break
        if score > best_score:
            best_score = score
            best_move = move
    print('depth reached:', current_depth)
    print('move:', best_move)
    print('score:', best_score)
    return best_move

def alphabeta(board: str, token: str, alpha: float, beta: float, depth: int, startTime: float, timeLimit: float) -> tuple[int|float, int|float|None]:
    global seenBoards
    if time.time() - startTime > timeLimit:
        return (float('-inf'), -2)
    eToken = "XO"[token == "X"]
    if "." not in board:
        return (1000 * (board.count(token) - board.count(eToken)), None)
    possibles: set[int] = possibleMoves(board, token)
    if not possibles:
        if not possibleMoves(board, eToken):
            # end game
            return (1000 * (board.count(token) - board.count(eToken)), None)
        if depth != 0:
            # pass turn
            nm = alphabeta(board, eToken, -beta, -alpha, depth, startTime, timeLimit)
            if nm[1] == -2:
                return nm
            seenBoards[(board, token)] = -nm[0]
            return (-nm[0], -1)
    if depth == 0:
        # depth limit reached
        # calculate score and return
        score = calculateBoardScore(board, token)
        seenBoards[(board, token)] = score
        return (score, None)
    maxTuple = (float("-inf"), None)
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
            if nm[1] == -2:
                return nm
            if -nm[0] > maxTuple[0]:
                maxTuple = (-nm[0], move)
                alpha = max(alpha, maxTuple[0])
            seenBoards[(newBoard, token)] = -nm[0]
        if alpha > beta:
            break
    return maxTuple

seenBoards = dict()
def calculateBoardScore(board: str, token: str):
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
    move_diff = len(possibleMoves(board, token)) - len(possibleMoves(board, eToken))
    return total + move_diff

def makeMove(moveIdx: int, board: str, toMove: str) -> str:
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

seenpsbls: dict[tuple[str, str], set[int]]  = {}
def possibleMoves(board: str, toMove: str) -> set[int]:
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
    possibleMoves: set[int] = set()
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

def removeBad(moves: set[int], board: str, token: str):
    moves_list = list(moves)
    for move in moves:
        if move in cxsquaresToCorner and board[cxsquaresToCorner[move]] != token:
            _ = moves_list.pop(moves_list.index(move))
    return set(moves)
