
import imp
import math
import time
import sys
import csv
import random
import multiprocessing as mp

#======================================================================
def BoardPrint(board,move=[],num =0 ):

    print("====== The current board(",num,")is (after move): ======")
    if move:
        print("move = ",move)
    for i in [7,6,5,4,3,2,1,0]:
        print(i,":", end=" ")
        for j in range(8):
            print(board[i][j], end=" ")
        print()
    print("   ",0,1,2,3,4,5,6,7)
    print("")

def BoardCopy(board):
    new_board = [[]]*8
    for i in range(8):
        new_board[i] = [] + board[i]
    return new_board

#======================================================================

def doit(move,state):
    new_state = BoardCopy(state)
    #Move one step
    #example: [(2,2),(3,3)] or [(2,2),(3,1)]
    if len(move) == 2 and abs(move[1][0] - move[0][0]) == 1:         
        new_state[move[0][0]][move[0][1]] = '.'
        if state[move[0][0]][move[0][1]] == 'b' and move[1][0] == 7:
            new_state[move[1][0]][move[1][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[1][0] == 0:
            new_state[move[1][0]][move[1][1]] = 'R'
        else:
            new_state[move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
    #Jump
    #example: [(1,1),(3,3),(5,5)] or [(1,1),(3,3),(5,1)]
    else:
        step = 0
        new_state[move[0][0]][move[0][1]] = '.'
        while step < len(move)-1:
            new_state[int(math.floor((move[step][0]+ move[step+1][0])/2))][int(math.floor((move[step][1]+ move[step+1][1])/2))] = '.'                        
            step = step+1
        if state[move[0][0]][move[0][1]] == 'b' and move[step][0] == 7:
            new_state[move[step][0]][move[step][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[step][0] == 0:
            new_state[move[step][0]][move[step][1]] = 'R'
        else:
            new_state[move[step][0]][move[step][1]] = state[move[0][0]][move[0][1]]
    return new_state

#======================================================================
# Initial_Board = [ ['b','.','b','.','b','.','b','.'],\
#                   ['.','b','.','b','.','b','.','b'],\
#                   ['b','.','b','.','b','.','b','.'],\
#                   ['.','.','.','.','.','.','.','.'],\
#                   ['.','.','.','.','.','.','.','.'],\
#                   ['.','r','.','r','.','r','.','r'],\
#                   ['r','.','r','.','r','.','r','.'],\
#                   ['.','r','.','r','.','r','.','r'] \
#                 ]

Initial_Board = [ ['.','b','.','b','.','b','.','b'],\
                  ['b','.','b','.','b','.','b','.'],\
                  ['.','b','.','b','.','b','.','b'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['.','.','.','.','.','.','.','.'],\
                  ['r','.','r','.','r','.','r','.'],\
                  ['.','r','.','r','.','r','.','r'],\
                  ['r','.','r','.','r','.','r','.'],\
                ]

# Initial_Board.reverse()

 # 7 : . r . r . r . r
 # 6 : r . r . r . r .
 # 5 : . r . r . r . r
 # 4 : . . . . . . . .
 # 3 : . . . . . . . .
 # 2 : b . b . b . b .
 # 1 : . b . b . b . b
 # 0 : b . b . b . b .
 #     0 1 2 3 4 5 6 7
#======================================================================
def countChessPieces (board):

    num_red = num_blk = 0
    for row in board:
        for cell in row:
            if cell == 'r':
                num_red += 1
            elif cell == 'R':
                num_red += 3
            elif cell == 'b':
                num_blk += 1
            elif cell == 'B':
                num_blk += 3

    return (num_red, num_blk)

#======================================================================

#======================================================================
def play(Aplayer, Bplayer, param_A, param_B, start_state = Initial_Board):

    A = Aplayer.Player('r')
    B = Bplayer.Player('b')

    A.loadParam(param_A)
    B.loadParam(param_B)
    
    currPlayer = A
    state = start_state
    board_num = 0

    num_red = num_blk = boardChanged = 0

    while True:
        # print("It is ", currPlayer ,"'s turn")

        move = currPlayer.nextMove(state)

        if not move:
            break

        # print("The move is : ",move, end=" ")
        # print(" (in %.2f ms)" % (elapse*1000), end=" ")
        #
        # print()
        #check_move
        state = doit(move,state)


        n_num_red, n_num_blk =  countChessPieces(state)

        if num_red == n_num_red and num_blk == n_num_blk:
            boardChanged += 1
            if boardChanged > 30:
                currPlayer = B if num_red > num_blk else A
                break
        else:
            boardChanged = 0
            num_red = n_num_red
            num_blk = n_num_blk


        board_num = board_num + 1


        if currPlayer == A:
            currPlayer = B
        else:
            currPlayer = A

    BoardPrint(state, num=board_num)

    if currPlayer == A:
        return 'b'
    else:
        return 'r'

if __name__ == "__main__":

    param_file = open('train_data/test_param_0.csv', "r")
    reader = csv.reader(param_file)
    data = [[[float(cell) if cell else None for cell in row], 0] for row in reader]

    Aplayer = imp.load_source('A_module', "checkers_2017_train" + ".py")
    Bplayer = imp.load_source('B_module', "checkers_2017_train" + ".py")

    NUMBER_OF_GENERATION = 2

    NUMBER_OF_PROCESS = 1
    # PROCESS_PARAM = [[0, 30]] # 1 process 30 pop
    PROCESS_PARAM = [[0, 30]]

    upper_bound = [40, 80, 15, 30, 30, 1.5]
    lower_bound = [15, 25, 0, 0, 0, 0]

    LOCAL_SIGMA = [(upper_bound[i] - lower_bound[i]) * 0.01 for  i in range(len(upper_bound))]
    SIGMA = [(upper_bound[i] - lower_bound[i]) * 0.5 for  i in range(len(upper_bound))]

    for i_gen in range(1, NUMBER_OF_GENERATION):

        lstProcessConn = []
        lstProcess = []

        def process_func(process_number, child_conn = None):

            start = PROCESS_PARAM[process_number][0]
            end = PROCESS_PARAM[process_number][1]

            for i in range(start, end):
                for j in range(i + 1, len(data)):

                    # Chon random ben di truoc

                    FIRST_MOVE_RATIO = 0.5

                    if random.random() < FIRST_MOVE_RATIO:
                        first_move = i
                        second_move = j
                    else:
                        first_move = j
                        second_move = i


                    # Danh 1 lan
                    start_time = time.time()
                    result = play(Aplayer, Bplayer, data[first_move][0], data[second_move][0])
                    if result == 'r':
                        data[first_move][1] += 1
                    else:
                        data[second_move][1] += 1

                    print('Player %i vs Player %i.\nWinner: Player %i in %f(s)' %
                          (first_move, second_move, first_move if result == 'r' else second_move, time.time() - start_time))
                    print ()

            if child_conn:
                child_conn.send(data)


        for j in range(NUMBER_OF_PROCESS - 1):
            parent_conn, child_conn = mp.Pipe()
            lstProcessConn.append((parent_conn, child_conn))

            nProcess = mp.Process(target=process_func, args=(j, child_conn))
            nProcess.start()
            lstProcess.append(nProcess)


        process_func(NUMBER_OF_PROCESS - 1)

        for process in lstProcess:
            process.join()

        # Fetch result from other processes
        for conn in lstProcessConn:
            parent_conn = conn[0]
            data_from_process = parent_conn.recv()

            # Add results to current data table
            j = 0
            for param, pts in data_from_process:
                data[j][1] += pts
                j += 1

        data.sort(key=lambda x: x[1], reverse=True)

        # match_result_file = open('train_data/test_result_' + str(i_gen - 1) + '.csv', 'w+')  #Local version
        match_result_file = open('/output/test_result_' + str(i_gen - 1) + '.csv', 'w+')  # Floyd version

        result_data = [row[0] + [row[1]] for row in data]

        result_writer = csv.writer(match_result_file)
        result_writer.writerows(result_data)
        match_result_file.close()

        # # Tao quan the moi
        # result_data = []
        #
        # sample_data = data[: int( len(data) / 2)]
        # fMax = data[0][1]
        # ndata = []
        #
        # # Create a new generation keeping the same size as the previous one
        # for i in range(len(data)):
        #     # Choose 2 random element from the current generation
        #     subdata = []
        #
        #     while len(subdata) < 2:
        #         row1, row2 = random.sample(sample_data, 2)
        #         # Selection with Stochastic acceptance
        #         # row[1] is number of victory for this player, used as fitness value of the player fi
        #         # then the probability for this player kept in the next generation is fi/fMax
        #         if random.random() < row1[1] / fMax and random.random() < row2[1] / fMax:
        #             subdata.append(row1[0])
        #             subdata.append(row2[0])
        #
        #     # Crossover & Mutation
        #     KEEP_A_RATIO = 0.5
        #     MUTATION_RATIO = 0.05
        #
        #     new_player = []
        #
        #     for j in range(6):
        #         new_value = None
        #         if random.random() < KEEP_A_RATIO:
        #             new_value = subdata[0][j]
        #         else:
        #             new_value = subdata[1][j]
        #
        #         if random.random() < MUTATION_RATIO:
        #             new_value = random.gauss(new_value, SIGMA[j])
        #         else:
        #             new_value = random.gauss(new_value, LOCAL_SIGMA[j])
        #
        #         new_player.append(new_value)
        #
        #     ndata.append(new_player)
        #
        # new_generation_param_file = open('train_data/test_param_' + str(i_gen) + '.csv', 'w+')  #Local version
        # # new_generation_param_file = open('/output/test_param_' + str(i_gen) + '.csv', 'w+')  #Floyd version
        # writer = csv.writer(new_generation_param_file)
        # writer.writerows(ndata)
        # new_generation_param_file.close()
        #
        # data = [[row, 0] for row in ndata]