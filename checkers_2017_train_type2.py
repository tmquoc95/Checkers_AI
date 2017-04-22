
import math
import time

# ======================= Global Variable and Constant Declaration ==============================

TRUE_SIDE_PARAM = None
END_TIME = None

PROCESSING_TIME = 2.6

ILL = 0     # Constant for illegal moves
MOV = 1     # Constant for legal forward move
CAP = 2     # Constant for legal capture

# Direction for row and col
NE = (-1, 1)  # North East
NW = (-1, -1)  # North West
SE = (1, 1)  # South East
SW = (1, -1)  # South West

# PIECE COLOR CONSTANT
RED = 'r'
BLK = 'b'

RED_K = 'R'
BLK_K = 'B'

RED_GRP = {RED, RED_K}
BLK_GRP = {BLK, BLK_K}

ALL_GRP = RED_GRP | BLK_GRP

EMPTY = '.'

# Point constants
MAN_PTS = 35
KING_PTS = 75
CONNECT_PTS = 1
ENEMY_PTS_RATIO = 0.8

RED_MAN_ROW_PTS = None
BLK_MAN_ROW_PTS = None
MAN_ROW_PTS_ratio = 1

MAN_COL_PTS = None
MAN_COL_PTS_ratio = 1

KING_ROW_PTS = None
KING_ROW_PTS_ratio = 1

KING_COL_PTS = None
KING_COL_PTS_ratio =1

RED_SIDE_PARAM = {'aMan': RED, 'aKing': RED_K, 'eMan': BLK, 'eKing': BLK_K,
                  'allies': RED_GRP, 'enemies': BLK_GRP, 'aManRowPts': None, 'eManRowPts': None}
BLK_SIDE_PARAM = {'aMan': BLK, 'aKing': BLK_K, 'eMan': RED, 'eKing': RED_K,
                  'allies': BLK_GRP, 'enemies': RED_GRP, 'aManRowPts': None, 'eManRowPts': None}

#============================ Common Function ========================

def checkValidCell(row, col):
    """Check whether this cell position is valid in chessboard (0 <= row, col <= 7)"""
    if row > -1 and row < 8 and col > -1 and col < 8:
        return True
    else:
        return False


def makeKing(board, row, col):
    cell = board[row][col]
    if cell == BLK and row == 7:
        board[row][col] = BLK_K
        return True
    elif cell == RED and row == 0:
        board[row][col] = RED_K
        return True
    return False

def copyBoard (board):
    return list (row[:] for row in board)

# ======================== Class Player =======================================
class Player:
    def __init__(self, str_name):

        self.str = str_name

        global TRUE_SIDE_PARAM
        if str_name == 'r':
            TRUE_SIDE_PARAM = RED_SIDE_PARAM
        else:
            TRUE_SIDE_PARAM = BLK_SIDE_PARAM

        self.buildPtsTable()

    def __str__(self):
        return self.str

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples
    def nextMove(self, state):
        global END_TIME

        # # Real matches version
        # END_TIME = time.time() + PROCESSING_TIME

        # # Train version
        END_TIME = +math.inf

        if self.str == RED:
            sidecolor = BLK
        else:
            sidecolor = RED

        board = Board(sidecolor, state)

        result = board.pickOneMove()

        return result

    def buildPtsTable(self):
        global KING_ROW_PTS, KING_COL_PTS, \
            RED_MAN_ROW_PTS, BLK_MAN_ROW_PTS, MAN_COL_PTS, RED_SIDE_PARAM, BLK_SIDE_PARAM

        row0_pts = 4
        row1_pts = 0
        row_inc_pts = 0.5

        BLK_MAN_ROW_PTS = [row0_pts] + [row1_pts + row_inc_pts* i  for i in range(7)]
        BLK_MAN_ROW_PTS = [MAN_ROW_PTS_ratio * i for i in BLK_MAN_ROW_PTS]

        # copy and reverse for other side
        RED_MAN_ROW_PTS = BLK_MAN_ROW_PTS[:]
        RED_MAN_ROW_PTS.reverse()

        RED_SIDE_PARAM['aManRowPts'] = RED_MAN_ROW_PTS
        RED_SIDE_PARAM['eManRowPts'] = BLK_MAN_ROW_PTS

        BLK_SIDE_PARAM['aManRowPts'] = BLK_MAN_ROW_PTS
        BLK_SIDE_PARAM['eManRowPts'] = RED_MAN_ROW_PTS

        # bang diem theo cot doi xung cho MAN
        col0_pts = 4
        col1_pts = 1
        col2_pts = 2
        col3_pts = 3

        MAN_COL_PTS = [col0_pts, col1_pts, col2_pts, col3_pts,
                       col3_pts, col2_pts, col1_pts, col0_pts]

        MAN_COL_PTS = [MAN_COL_PTS_ratio * i for i in MAN_COL_PTS]

        # bang diem theo hang doi xung cho KING
        row0_pts = 1
        row1_pts = 2
        row2_pts = 3
        row3_pts = 4

        KING_ROW_PTS = [row0_pts, row1_pts, row2_pts, row3_pts,
                        row3_pts, row2_pts, row1_pts, row0_pts]

        KING_ROW_PTS = [KING_ROW_PTS_ratio * i for i in KING_ROW_PTS]

        # bang diem theo cot cho KING
        col0_pts = 1
        col1_pts = 2
        col2_pts = 3
        col3_pts = 4

        KING_COL_PTS = [col0_pts, col1_pts, col2_pts, col3_pts,
                        col3_pts, col2_pts, col1_pts, col0_pts]

        KING_COL_PTS = [KING_COL_PTS_ratio * i for i in KING_COL_PTS]

    def loadParam(self, params):

        global MAN_PTS, KING_PTS, CONNECT_PTS, ENEMY_PTS_RATIO, \
        MAN_ROW_PTS_ratio, MAN_COL_PTS_ratio, KING_ROW_PTS_ratio, KING_COL_PTS_ratio

        if params[0]:
            MAN_PTS = params[0]

        if params[1]:
            KING_PTS = params[1]

        if params[2]:
            CONNECT_PTS = params[2]

        if params[3]:
            ENEMY_PTS_RATIO = params[3]

        if params[4]:
            MAN_ROW_PTS_ratio = params[4]

        if params[5]:
            MAN_COL_PTS_ratio = params[5]

        if params[6]:
            KING_ROW_PTS_ratio = params[6]

        if params[7]:
            KING_COL_PTS_ratio = params[7]

        self.buildPtsTable()

        print (MAN_PTS, KING_PTS, CONNECT_PTS, ENEMY_PTS_RATIO, \
               MAN_ROW_PTS_ratio, MAN_COL_PTS_ratio, KING_ROW_PTS_ratio, KING_COL_PTS_ratio)

#============================= Board Class ============================================
class Board:

    def __init__(self, sidecolor, board):
        if sidecolor == RED:
            self.nodeParam = RED_SIDE_PARAM
            self.childParam = BLK_SIDE_PARAM
        else:
            self.nodeParam = BLK_SIDE_PARAM
            self.childParam = RED_SIDE_PARAM

        self.isTrueSide = (self.nodeParam == TRUE_SIDE_PARAM)
        self.eval_pts = None
        self.board = board  #Board is 2-dimensional list
        self.moveList = []
        self.hasBuiltMoveList = False

    def checkMove(self):
        def checkMove_OneDir(row, col, direction, data):
            """Check whether 1 move can be made in a specific direction from current position"""
            flag, locs, iboard = data
            type = iboard[row][col]

            nrow = row + direction[0]
            ncol = col + direction[1]

            if checkValidCell(nrow, ncol):
                if board[nrow][ncol] == EMPTY:
                    nboard = copyBoard(iboard)
                    nboard[row][col] = EMPTY
                    nboard[nrow][ncol] = type
                    makeKing(nboard, nrow, ncol)

                    ndata = [MOV, locs + [(nrow, ncol)], Board(self.childParam['aMan'], nboard)]
                    self.moveList.append(ndata)
                    return MOV

            return ILL

        def checkMove_MultiDir(row, col, data):
            """Check avaiable moves in many direction from current position"""
            flag, locs, iboard = data
            type = iboard[row][col]

            if type == RED_K or type == BLK_K:
                checkMove_OneDir(row, col, NW, data)
                checkMove_OneDir(row, col, NE, data)
                checkMove_OneDir(row, col, SW, data)
                checkMove_OneDir(row, col, SE, data)
            elif type == RED:
                checkMove_OneDir(row, col, NW, data)
                checkMove_OneDir(row, col, NE, data)
            else:
                checkMove_OneDir(row, col, SW, data)
                checkMove_OneDir(row, col, SE, data)

        board = self.board
        for row in range(8):
            for col in range(8):
                if board[row][col] in self.childParam["allies"]:
                    ndata = (ILL, [(row, col)], board)
                    checkMove_MultiDir(row, col, ndata)

    def checkCapture(self):

        # data parameter consist of a CAP or ILL flag, 1 list of cell, 1 new board
        def checkCapture_OneDir(row, col, direction, data):

            flag, locs, iboard = data
            type = iboard[row][col]

            mrow = row + direction[0]  # Middle cell
            mcol = col + direction[1]

            trow = mrow + direction[0]  # Target cell
            tcol = mcol + direction[1]

            if checkValidCell(mrow, mcol) and checkValidCell(trow, tcol):
                if iboard[trow][tcol] == EMPTY and iboard[mrow][mcol] in self.childParam["enemies"]:
                    nboard = copyBoard(iboard)
                    nboard[row][col] = EMPTY
                    nboard[mrow][mcol] = EMPTY
                    nboard[trow][tcol] = type
                    ndata = [CAP, locs + [(trow, tcol)], nboard]

                    if makeKing(nboard, trow, tcol):
                        ndata = ndata[0:2] + [Board(self.childParam['aMan'], nboard)]
                        self.moveList.append(ndata)
                        return CAP
                    else:
                        return checkCapture_MultiDir(trow, tcol, ndata)
            return ILL


        def checkCapture_MultiDir(row, col, data):

            flag, locs, iboard = data
            type = iboard[row][col]
            ndata = (ILL, locs, iboard)
            NWres = NEres = SWres = SEres = ILL

            if type == RED_K or type == BLK_K:
                NWres = checkCapture_OneDir(row, col, NW, ndata)
                NEres = checkCapture_OneDir(row, col, NE, ndata)
                SWres = checkCapture_OneDir(row, col, SW, ndata)
                SEres = checkCapture_OneDir(row, col, SE, ndata)
            elif type == RED:
                NWres = checkCapture_OneDir(row, col, NW, ndata)
                NEres = checkCapture_OneDir(row, col, NE, ndata)
            else:
                SWres = checkCapture_OneDir(row, col, SW, ndata)
                SEres = checkCapture_OneDir(row, col, SE, ndata)

            Mixres = NWres | NEres | SWres | SEres

            if Mixres == 0 and flag == CAP:
                ndata = (flag, locs, Board(self.childParam['aMan'], iboard))
                self.moveList.append(ndata)

            return (Mixres | flag)

        board = self.board
        for row in range(8):
            for col in range(8):
                if board[row][col] in self.childParam["allies"]:
                    ndata = (ILL, [(row, col)], board)
                    checkCapture_MultiDir(row, col, ndata)

    def buildMoveList(self):

        # Force Jump
        self.checkCapture()
        if len(self.moveList) == 0:
            self.checkMove()

        # # Do not force jump
        # self.checkCapture()
        # self.checkMove()

        self.hasBuiltMoveList = True

    def evalOneBoard(self):  # target is either (RED, RED_K, RED_GRP) or (BLK, BLK_K, BLK_GRP)
        if len(self.moveList) == 0:
            if (self.isTrueSide):
                return math.inf
            else:
                return -math.inf

        pts_aMan = pts_aKing = pts_aConnect = pts_aPosition = \
            pts_eMan = pts_eKing = pts_eConnect = pts_ePosition = 0

        sideParam = TRUE_SIDE_PARAM
        iboard = self.board

        for row in range(8):
            for col in range(8):
                cell = iboard[row][col]

                if cell == sideParam['aMan']:  # man pieces
                    pts_aMan += MAN_PTS
                    pts_aPosition += sideParam['aManRowPts'][row] + MAN_COL_PTS[col]

                    for direction in {NW, NE, SW, SE}:
                        nrow = row + direction[0]
                        ncol = col + direction[1]

                        if checkValidCell(nrow, ncol):
                            if iboard[nrow][ncol] in sideParam['allies']:
                                pts_aConnect += CONNECT_PTS

                if cell == sideParam['aKing']:
                    pts_aKing += KING_PTS
                    pts_aPosition += KING_ROW_PTS[row] + KING_COL_PTS[col]

                if cell == sideParam['eMan']:  # man pieces
                    pts_eMan += MAN_PTS
                    pts_ePosition += sideParam['eManRowPts'][row] + MAN_COL_PTS[col]

                    for direction in {NW, NE, SW, SE}:
                        nrow = row + direction[0]
                        ncol = col + direction[1]

                        if checkValidCell(nrow, ncol):
                            if iboard[nrow][ncol] in sideParam['enemies']:
                                pts_eConnect += CONNECT_PTS

                if cell == sideParam['eKing']:
                    pts_eKing += KING_PTS
                    pts_ePosition += KING_ROW_PTS[row] + KING_COL_PTS[col]

        pts = (pts_aMan + pts_aKing + pts_aConnect + pts_aPosition) \
              / (pts_eMan + pts_eKing)

        pts -= ENEMY_PTS_RATIO * (pts_eMan + pts_eKing + pts_eConnect + pts_ePosition) \
               / (pts_aMan + pts_aKing)

        return pts

    def minimax (self, depth, alpha, beta):
        if time.time() >= END_TIME:
            raise TimeUp()

        if not self.hasBuiltMoveList:
            self.buildMoveList()

        if depth <= 0:
            self.eval_pts = self.evalOneBoard()
            return self.eval_pts

        if not self.isTrueSide:
            v = -math.inf
            for row in self.moveList:
                flag, locs, board = row
                v = max(v, board.minimax(depth - 1, alpha, beta))
                alpha = max(alpha, v)
                if beta <= alpha:
                    break
        else:
            v = +math.inf
            for row in self.moveList:
                flag, locs, board = row
                v = min(v, board.minimax(depth - 1, alpha, beta))
                beta = min(beta, v)
                if beta <= alpha:
                    break

        self.eval_pts = v
        return self.eval_pts

    def pickOneMove(self):

        # # For REAL MATCHES
        # MINIMAX_DEPTH = 3
        #
        # try:
        #     while True:
        #         self.minimax(MINIMAX_DEPTH, -math.inf, +math.inf)
        #         MINIMAX_DEPTH += 2
        # except (TimeUp):
        #     pass
        #
        # print (MINIMAX_DEPTH)

        # # For TRAINING MATCHES
        self.minimax(5, -math.inf, +math.inf)

        self.moveList.sort(key=lambda x: x[2].eval_pts if x[2].eval_pts else -math.inf, reverse=True)

        try:
            flag, locs, board = self.moveList[0]
            return locs
        except:
            return []

    def MoveListPrint (self):
        def printBoard(board):

            # print("====== The current board(", num, ")is (after move): ======")
            # if move:
            #     print("move = ", move)
            for i in [7, 6, 5, 4, 3, 2, 1, 0]:
                print(i, ":", end=" ")
                for j in range(8):
                    print(board[i][j], end=" ")
                print()
            print("   ", 0, 1, 2, 3, 4, 5, 6, 7)
            print("")

        for move in self.moveList:
            type, step, board = move
            print (type)
            print (step)
            printBoard(board)


class TimeUp(Exception):
    pass


