#Othello board important indices
corners = {0, 7, 63, 56}
edges = {
    x for x in range(64) if x // 8 == 0 or x // 8 == 7 or x % 8 == 0 or x % 8 == 7
} - corners
xsquares = {9, 14, 49, 54}
csquares = {1, 6, 8, 15, 48, 55, 57, 62}
asquares = {2, 5, 16, 23, 40, 47, 58, 61}
cornerDirections: dict[int, list[int]] = dict()
cornerDirections[0] = [1, 8]
cornerDirections[7] = [-1, 8]
cornerDirections[63] = [-1, -8]
cornerDirections[56] = [1, -8]
asquarePairs: dict[int, int] = dict()
asquarePairs[2] = 5
asquarePairs[5] = 2
asquarePairs[16] = 40
asquarePairs[40] = 16
asquarePairs[23] = 47
asquarePairs[47] = 23
asquarePairs[58] = 61
asquarePairs[61] = 58
bsquares = {3, 4, 24, 31, 32, 39, 59, 60}
center4 = {27, 28, 35, 36}


neighbors: list[list[int]] = []
for k in range(64):
    curr: list[int] = []
    if k % 8 != 7: curr.append(k+1)
    if k % 8 != 0: curr.append(k-1)
    if k-8 >= 0: curr.append(k-8)
    if k+8 <= 63: curr.append(k+8)
    if k+9 <= 63: curr.append(k+9)
    if k-9 >= 0: curr.append(k-9)
    if k+7 <= 63: curr.append(k+7)
    if k-7 >= 0: curr.append(k-7)
    neighbors.append(curr)

cxsquaresToCorner: dict[int, int] = dict()
for move in xsquares.union(csquares):
    for idx in neighbors[move]:
        for corner in corners:
            if idx == corner:
                cxsquaresToCorner[move] = corner

rays = [[idx - k for idx in neighbors[k]] for k in range(64)]
bounds: list[list[int]] = []
for idx in range(64):
    tmp: list[int] = []
    for diff in rays[idx]:
        nextIdx = idx + diff
        if abs(diff) == 8:  # vertical case
            while nextIdx >= 0 and nextIdx <= 63:
                nextIdx += diff
            nextIdx -= diff
        else:
            while (
                nextIdx >= 0 and nextIdx <= 63 and nextIdx % 8 != 0 and nextIdx % 8 != 7
            ):
                nextIdx += diff
            if nextIdx < 0 or nextIdx > 63:
                nextIdx -= diff
        tmp.append(nextIdx)
    bounds.append(tmp)
