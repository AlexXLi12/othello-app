import sys; args = sys.argv[1:]
#Alex Li Pd. 6
LIMIT_AB = 14
import time, random, re;
def setGlobals():
    global board, toMove, moves, neighbors
    board = ''
    toMove = ''
    moves = []
    while args:
        if re.search(r'^[oxOX.]{64}$', args[0]):
            board = args[0].upper()
            args.pop(0)
        elif re.search(r'^[oxOX]$', args[0]):
            toMove = args[0].upper()
            args.pop(0)
        else:
            moves += [int(args[0][i:i+2]) if '_' not in args[0][i:i+2] else int(args[0][i+1])for i in range(0,len(args[0]), 2)]
            args.pop(0)
    if not board:
        board = '.'*27+'OX......XO'+'.'*27
    if not toMove:
        pieces = board.count('X') + board.count('O')
        toMove = ['X','O'][pieces%2]
    if not possibleMoves(board, toMove):
        toMove = 'XO'[toMove=='X']
corners = {0,7,63,56}
edges = {x for x in range(64) if x//8 == 0 or x // 8 == 7 or x % 8 == 0 or x % 8 == 7} - corners
xsquares = {9, 14, 49, 54}                                                              
csquares = {1, 6, 8, 15, 48, 55, 57, 62}
asquares = {2, 5, 16, 23, 40, 47, 58, 61}
ecol0 = 9187201950435737471 #excluding col 0
ecol7 = 18374403900871474942 #excluding col 7
filled = 18446744073709551615 # all bits set
col7 = filled ^ ecol7

def shift(bboard, direction):
    if direction in (-1,-9):
        return bboard >> abs(direction) & ecol0
    if direction == 7:
        return bboard << 7 & ecol0
    if direction in (1,9):
        return bboard << direction & ecol7
    if direction == -7:
        return bboard >> 7 & ecol0
    if direction == -8:
        return bboard >> 8 
    return bboard << 8 & filled

numToMoves = []
for i in range(256):
    temp = []
    currIndex = 0
    while i:
        if i & 1:
            temp.append(currIndex)
        currIndex += 1
        i >>= 1
    numToMoves.append(temp)
setBitsCount = []
for i in range(256):
    count = 0
    while i:
        count += i&1
        i >>= 1
    setBitsCount.append(count)

def possibleMoves(board, token):
    if len(board) == 2:
        xInt, oInt = board
    else:
        xInt, oInt = boardToInt(board)
    empty = filled ^ (xInt | oInt)
    if token == 'X':
        tknInt = xInt
        eInt = oInt
    else:
        tknInt = oInt
        eInt = xInt
    upsbls = 0 #up
    tmp = tknInt
    while tmp:
        tmp = tmp << 8 & eInt
        upsbls |= tmp
    upsbls = upsbls << 8 & empty
    dpsbls = 0 #down
    tmp = tknInt
    while tmp:
        tmp = tmp >> 8 & eInt
        dpsbls |= tmp
    dpsbls = dpsbls >> 8 & empty
    lpsbls = 0 #left
    tmp = tknInt
    while tmp:
        tmp = tmp << 1 & ecol7 & eInt
        lpsbls |= tmp
    lpsbls = lpsbls << 1 & ecol7 & empty
    rpsbls = 0 #right
    tmp = tknInt
    while tmp:
        tmp = tmp >> 1 & ecol0 & eInt
        rpsbls |= tmp
    rpsbls = rpsbls >> 1 & ecol0 & empty
    sepsbls = 0 #SE
    tmp = tknInt
    while tmp:
        tmp = tmp >> 9 & ecol0 & eInt
        sepsbls |= tmp
    sepsbls = sepsbls >> 9 & ecol0 & empty
    swpsbls = 0 #SW
    tmp = tknInt
    while tmp:
        tmp = tmp >> 7 & ecol7 & eInt
        swpsbls |= tmp
    swpsbls = swpsbls >> 7 & ecol7 & empty
    nepsbls = 0 #NE
    tmp = tknInt
    while tmp:
        tmp = tmp << 7 & ecol0 & eInt
        nepsbls |= tmp
    nepsbls = nepsbls << 7 & ecol0 & empty
    nwpsbls = 0 #NW
    tmp = tknInt
    while tmp:
        tmp = tmp << 9 & ecol7 & eInt
        nwpsbls |= tmp
    nwpsbls = nwpsbls << 9 & ecol7 & empty
    psbls = upsbls | dpsbls | rpsbls | lpsbls | swpsbls | sepsbls | nwpsbls | nepsbls
    return psbls

stripPossibles = []
for i in range(8):
    temp1 = 1 << i
    temp2 = 1 << i * 8
    for k in range(7):
        temp1 |= temp1 << 8
        temp2 |= temp2 << 1
    stripPossibles.append(temp1)
    stripPossibles.append(temp2)
for i in range(6):
    temp1 = 1 << i
    temp2 = 1 << (7-i)
    temp3 = 1 << (i*8)
    temp4 = 1 << (i*8+7)
    for k in range(7):
        temp1 |= shift(temp1, 9)
        temp2 |= shift(temp2, 7)
        temp3 |= shift(temp3, 9)
        temp4 |= shift(temp4, 7)
    stripPossibles.append(temp1)
    stripPossibles.append(temp2)
    stripPossibles.append(temp3)
    stripPossibles.append(temp4)

def getPositions(intBoard):
    pos = set()
    ind = 0
    for i in range(8):
        curr = intBoard & 255
        for idx in numToMoves[curr]:
            pos.add(ind+idx)
        intBoard >>= 8
        ind += 8
    return pos

def twoD_binary(intBoard):
    bboard = f'{intBoard:64b}'
    s = ''
    for i in range(64):
        if bboard[i] == '1':
            s += '1'
        else:
            s+= '0'
        if (i + 1) % 8 == 0:
            s += '\n'
    return s
ct = 0
def makeStrips(indexList, intBrd, pDict):
    global st, ct
    ct += 1
    if not indexList:
        return pDict
    if intBrd not in pDict:
        pDict[intBrd] = getPositions(possibleMoves(intBrd, 'X'))
    if indexList:
        makeStrips(indexList[1:], (intBrd[0] | 1 << indexList[0], intBrd[1]), pDict)
        makeStrips(indexList[1:], (intBrd[0], intBrd[1] | 1 << indexList[0]), pDict)
        makeStrips(indexList[1:], intBrd, pDict)
    return pDict

def makeVStrips(indexList, intBrd, pDict):
    if not indexList:
        return pDict
    if intBrd not in pDict:
        pDict[intBrd] = getPositions(possibleMoves(intBrd, 'X'))
        tmp = intBrd
        for i in range(7):
            tmp = (shift(tmp[0],1), tmp[1])
            pDict[tmp] = {idx + i for idx in pDict[intBrd]}
    if indexList:
        makeVStrips(indexList[1:], (intBrd[0] | 1 << indexList[0], intBrd[1]), pDict)
        makeVStrips(indexList[1:], (intBrd[0], intBrd[1] | 1 << indexList[0]), pDict)
        makeVStrips(indexList[1:], intBrd, pDict)
    return pDict

def makeHStrips(indexList, intBrd, pDict):
    if not indexList:
        return pDict
    if intBrd not in pDict:
        pDict[intBrd] = getPositions(possibleMoves(intBrd, 'X'))
        tmp = intBrd
        for i in range(7):
            tmp = (shift(tmp[0],8), tmp[1])
            pDict[tmp] = {idx + i*8 for idx in pDict[intBrd]}
    if indexList:
        makeHStrips(indexList[1:], (intBrd[0] | 1 << indexList[0], intBrd[1]), pDict)
        makeHStrips(indexList[1:], (intBrd[0], intBrd[1] | 1 << indexList[0]), pDict)
        makeHStrips(indexList[1:], intBrd, pDict)
    return pDict

possiblesDict = dict() #all combinations of strips
#make vertical strips
start = time.process_time()
indexes = list(getPositions(stripPossibles[0]))
tknInt = eInt = 0
possiblesDict = makeVStrips(indexes, (tknInt,eInt), possiblesDict)
#make horizontal strips
indexes = list(getPositions(stripPossibles[1]))
tknInt = eInt = 0
possiblesDict = makeHStrips(indexes, (tknInt,eInt), possiblesDict)
#make diagonal strips
for strip in stripPossibles[18:]:
    indexes = list(getPositions(strip))
    tknInt = eInt = 0
    possiblesDict = makeStrips(indexes, (tknInt,eInt), possiblesDict)
stop = time.process_time()
print('finished', stop-start, len(possiblesDict))


def possiblesLookUp(bboard):
    possibles = set()
    for strip in stripPossibles:
        possibles = {*possibles, *possiblesDict[(bboard[0]&strip, bboard[1]&strip)]}
    return possibles

neighbors = []
for k in range(64):
    curr = set()
    if k % 8 != 7: curr.add(k+1)
    if k % 8 != 0: curr.add(k-1)
    if k-8 >= 0: curr.add(k-8)
    if k+8 <= 63: curr.add(k+8)
    if k+9 <= 63 and k%8 != 7: curr.add(k+9)
    if k-9 >= 0 and k%8 != 0: curr.add(k-9)
    if k+7 <= 63 and k%8 != 0: curr.add(k+7)
    if k-7 >= 0 and k%8 != 7: curr.add(k-7)
    neighbors.append(curr)

srays = [[idx-k for idx in neighbors[k]] for k in range(64)]
rays = []
bounds = []
for idx in range(64):
    temp = []
    for diff in srays[idx]:
        tmp = 0
        nextIdx = idx + diff
        if nextIdx % 8 in (0,7) and abs(diff) != 8:
            continue
        tmp |= (1 << nextIdx)
        temp.append((tmp, diff))
    rays.append(temp)

cxsquaresToCorner = dict()
for move in xsquares.union(csquares):
    for idx in neighbors[move]:
        for corner in corners:
            if idx == corner:
                cxsquaresToCorner[move] = corner

def setPossibles(board, possibleMoves):
    lst = list(board)
    for idx in possibleMoves:
        lst[idx] = '*'
    return ''.join(lst)

def twoD_Output(board):
    s = ''
    for k in range(8):
        s += f'{board[k*8:(k+1)*8]}\n'
    return s[:-1] #get rid of last newline

def scoreBoard(board, token):
    tknBoard = board[token == 'O']
    count = 0
    while (tknBoard):
        count += setBitsCount[tknBoard&255]
        tknBoard = tknBoard >> 8
    return count

def intToBoard(intBoard):
    sBoard = ''
    xBoard, oBoard = intBoard
    for i in range(64):
        if xBoard & 1:
            sBoard += 'X'
        elif oBoard & 1:
            sBoard += 'O'
        else:
            sBoard += '.'
        xBoard >>= 1
        oBoard >>= 1
    return sBoard

def makeMove(moveIdx, board, toMove):
    conv = False
    if len(board) > 2:
        conv = True
        board = boardToInt(board)
    tknBoard = board[toMove == 'O']
    eBoard = board[toMove == 'X']
    for ray, diff in rays[moveIdx]:
        if not ray & eBoard:
            continue
        idx = moveIdx+diff
        rayc = ray
        while rayc & eBoard:
            rayc = shift(rayc, diff)
            idx += diff
        if 0 <= idx and idx != moveIdx + diff and (1 << idx) & tknBoard:
            for i in range(moveIdx, idx, diff):
                tknBoard |= 1 << i
    eBoard ^= (eBoard & tknBoard)
    bboard = ()
    if toMove == 'X':
        bboard = (tknBoard, eBoard)
    else:
        bboard = (eBoard, tknBoard)
    if conv:
        return intToBoard(bboard)
    return bboard

def pString(possibles):
    s = ''
    for p in possibles:
        s += f'{p}, '
    return s[:-2]

def minimizeEnemy(idx_list, board, token):
    if not idx_list:
        return
    opposite = list({'X','O'}-{token})[0]
    moveCt = list()
    for idx in idx_list:
        newBoard = makeMove(idx, board, token)
        possibles = removeBad(getPositions(possibleMoves(newBoard,opposite)), board, opposite)
        moveCt.append((len(possibles), idx))
    tpl = min(moveCt)
    return tpl[1]

#return set of good CX moves
def goodCX(moves, board, token):
    possibles = set()
    for move in moves:
        if move in cxsquaresToCorner and board[cxsquaresToCorner[move]] == token:
            possibles.add(move)
    return possibles

def removeBad(moves, board, token):
    moves = list(moves)
    for move in moves:
        if move in cxsquaresToCorner and board[cxsquaresToCorner[move]] != token:
            moves.pop(moves.index(move))
    return set(moves)

def preventEnemyCorners(moves, board, token):
    opposite = list({'X', 'O'} - {token})[0]
    goodMoves = set()
    cornerCount = len(corners & getPositions(possibleMoves(board, opposite)))
    for move in moves:
        newBoard = makeMove(move, board, token)
        ePossibles = getPositions(possibleMoves(newBoard,opposite))
        if len(corners & ePossibles) > cornerCount:
            continue
        goodMoves.add(move)
    return goodMoves

def preventDeadEnds(moves, board, token):
    opposite = list({'X', 'O'} - {token})[0]
    goodMoves = set()
    deadEnd = False
    for move in moves:
        newBoard = makeMove(move, board, token)
        ePossibles = getPositions(possibleMoves(newBoard,opposite))
        for emove in ePossibles:
            eBoard = makeMove(emove, newBoard, opposite)
            if eBoard.count(token) == 0:
                deadEnd = True
                break
        if deadEnd:
            deadEnd = False
            continue
        goodMoves.add(move)        
    return goodMoves

def boardToInt(board):
    xInt, oInt = 0, 0
    for i in range(64):
        if board[i] == 'X':
            xInt |= 1 << i
        elif board[i] == 'O':
            oInt |= 1 << i
    return (xInt, oInt)

seenBoards = dict()
count = 0
def sortMoves(possibles):
    cnrs = [*possibles&corners]
    asqrs = [*possibles&asquares]
    rest = possibles-corners
    return [*cnrs, *asqrs,*rest]
    
def main():
    print(twoD_binary(ecol7))

if __name__ == "__main__":
    main()