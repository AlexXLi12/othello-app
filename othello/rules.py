from .classes import Square

neighbors = []
for k in range(64):
    curr = []
    if k % 8 != 7: curr.append(k+1)
    if k % 8 != 0: curr.append(k-1)
    if k-8 >= 0: curr.append(k-8)
    if k+8 <= 63: curr.append(k+8)
    if k+9 <= 63: curr.append(k+9)
    if k-9 >= 0: curr.append(k-9)
    if k+7 <= 63: curr.append(k+7)
    if k-7 >= 0: curr.append(k-7)
    neighbors.append(curr)
def possibleMoves(board:list, player:int):
    """Return the list of indices of possible moves for the player specified.

    Args:
        board (list): list of Square objects representing the Othello board
        player (int): specifies whose turn it is (-1 == black, 1 == white)

    Returns:
        list(int): list of integers representing indices on the game board
    """
    opposite = player*-1
    tokens = [index for index, square in enumerate(board) if square.player == player] #get index of all positions of piece to move
    toCheck = [] # (idx of toMove, idx of opposing neighbor)
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
        board (list): _description_
        player (int): _description_
        move (int): _description_
    """