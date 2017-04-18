import math
import time

INF = 9999999
OVER_TIME = -1


def check_valid_loc(i, j):
    return i >= 0 and i <= 7 and j >= 0 and j <= 7


def is_jump(move):
    return abs(move[0][0] - move[1][0]) == 2


def varian(locations):
    if len(locations) <= 1:
        return 0
    mean = [0,0]
    for item in locations:
        mean[0] += item[0]
        mean[1] += item[1]
    mean[0] /= len(locations)
    mean[1] /= len(locations)

    res = 0
    for item in locations:
        res += math.sqrt((item[0]-mean[0])*(item[0]-mean[0]) + (item[1]-mean[1])*(item[1]-mean[1]))
    return res

def dot_product(a, b):
    res = 0
    for i in range(len(a)):
        res += a[i]*b[i]
    return res


def BoardCopy(board):
    new_board = [[]] * 8
    for i in range(8):
        new_board[i] = [] + board[i]
    return new_board


# example: [(1,1),(3,3)]
def jump_one(state, move):
    new_state = BoardCopy(state)
    new_state[move[0][0]][move[0][1]] = '.'
    new_state[int(math.floor((move[0][0] + move[1][0]) / 2))][int(math.floor((move[0][1] + move[1][1]) / 2))] = '.'
    new_state[move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
    return new_state


# do one move
def doit(move, state):
    new_state = BoardCopy(state)
    # Move one step
    # example: [(2,2),(3,3)] or [(2,2),(3,1)]
    if len(move) == 2 and abs(move[1][0] - move[0][0]) == 1:
        new_state[move[0][0]][move[0][1]] = '.'
        if state[move[0][0]][move[0][1]] == 'b' and move[1][0] == 7:
            new_state[move[1][0]][move[1][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[1][0] == 0:
            new_state[move[1][0]][move[1][1]] = 'R'
        else:
            new_state[move[1][0]][move[1][1]] = state[move[0][0]][move[0][1]]
    # Jump
    # example: [(1,1),(3,3),(5,5)] or [(1,1),(3,3),(5,1)]
    else:
        step = 0
        new_state[move[0][0]][move[0][1]] = '.'
        while step < len(move) - 1:
            new_state[int(math.floor((move[step][0] + move[step + 1][0]) / 2))][
                int(math.floor((move[step][1] + move[step + 1][1]) / 2))] = '.'
            step = step + 1
        if state[move[0][0]][move[0][1]] == 'b' and move[step][0] == 7:
            new_state[move[step][0]][move[step][1]] = 'B'
        elif state[move[0][0]][move[0][1]] == 'r' and move[step][0] == 0:
            new_state[move[step][0]][move[step][1]] = 'R'
        else:
            new_state[move[step][0]][move[step][1]] = state[move[0][0]][move[0][1]]
    return new_state


# ======================== Class Player =======================================
class Player:
    def __init__(self, str_name, heuristic_fun=1, strategy=1):
        self.str = str_name
        self.heuristic_fun = heuristic_fun
        self.strategy = strategy

    def __str__(self):
        return self.str

    def normal_enemy(self):
        if self.str.lower() == 'b':
            return Player('r')
        if self.str.lower() == 'r':
            return Player('b')

    def level_up(self, i):
        return (self.str == 'b' and i == 7) or (self.str == 'r' and i == 0)

    def terminal(self, state, color):
        return not self.move_gen(state, color)

    def valid_dir(self, state, i, j):
        res = []
        if self.str == 'b':
            if state[i][j].lower() == 'b':
                if check_valid_loc(i + 1, j + 1):
                    res += [[1, 1]]
                if check_valid_loc(i + 1, j - 1):
                    res += [[1, -1]]
                if state[i][j] == 'B':
                    if check_valid_loc(i - 1, j + 1):
                        res += [[-1, 1]]
                    if check_valid_loc(i - 1, j - 1):
                        res += [[-1, -1]]
        if self.str == 'r':
            if state[i][j].lower() == 'r':
                if check_valid_loc(i - 1, j + 1):
                    res += [[-1, 1]]
                if check_valid_loc(i - 1, j - 1):
                    res += [[-1, -1]]
                if state[i][j] == 'R':
                    if check_valid_loc(i + 1, j + 1):
                        res += [[1, 1]]
                    if check_valid_loc(i + 1, j - 1):
                        res += [[1, -1]]
        return res

    def valid_move(self, state, i, j, first):
        res = []
        current_valid_dir = self.valid_dir(state, i, j)
        for [i_dir, j_dir] in current_valid_dir:
            if first and state[i + i_dir][j + j_dir] == '.':
                res += [[(i, j), (i + i_dir, j + j_dir)]]
            elif state[i + i_dir][j + j_dir].lower() == self.normal_enemy().str:
                if check_valid_loc(i + 2 * i_dir, j + 2 * j_dir):
                    if state[i + 2 * i_dir][j + 2 * j_dir] == '.':
                        temp = []
                        if first:
                            temp += [(i, j), (i + 2 * i_dir, j + 2 * j_dir)]
                        else:
                            temp += [(i + 2 * i_dir, j + 2 * j_dir)]
                        new_state = jump_one(state, [(i, j), (i + 2 * i_dir, j + 2 * j_dir)])
                        valid_move_new_state = self.valid_move(new_state, i + 2 * i_dir, j + 2 * j_dir, False)
                        if not valid_move_new_state:
                            res += [temp]
                        else:
                            for move in valid_move_new_state:
                                res += [temp + move]
        return res

    def move_gen(self, state, color):
        res = []
        valid_move = []
        for i in range(8):
            for j in range(8):
                if color == 1:
                    valid_move += self.valid_move(state, i, j, True)
                else:
                    valid_move += self.normal_enemy().valid_move(state, i, j, True)
        #check jump
        have_jump = False
        for move in valid_move:
            if is_jump(move):
                have_jump = True
                break
        if have_jump:
            for move in valid_move:
                if is_jump(move):
                    res += [move]
        else:
            res = valid_move
        return res

    def heuristic(self, state, depth_ori):
        num_enemy_normal = 0
        num_enemy_king = 0
        num_ally_normal = 0
        num_ally_king = 0

        ally_locations = []
        enemy_locations = []

        for i in range(8):
            for j in range(8):
                if state[i][j] == self.str:
                    num_ally_normal += 1
                    ally_locations += [[i,j]]
                elif state[i][j] == self.str.upper():
                    num_ally_king += 1
                    ally_locations += [[i, j]]
                elif state[i][j] == self.normal_enemy().str:
                    num_enemy_normal += 1
                    enemy_locations += [[i, j]]
                elif state[i][j] == self.normal_enemy().str.upper():
                    num_enemy_king += 1
                    enemy_locations += [[i, j]]

        ally_varian = varian(ally_locations)
        enemy_varian = varian(enemy_locations)

        flexibility = 0
        if depth_ori % 2 == 0:
            flexibility = len(self.move_gen(state,1))
        else:
            flexibility = -len(self.move_gen(state,-1))

        feature = [num_ally_king - num_enemy_king,
                   num_ally_normal - num_enemy_normal,
                   ally_varian - enemy_varian,
                   flexibility]
        weight = [0, 0, 0, 0]
        if self.heuristic_fun == 1:
            weight = [1,1,0,0]
        elif self.heuristic_fun == 2:
            weight = [0.5,1,0,0]
        elif self.heuristic_fun == 3: #only flexibility of enemy
            weight = [1.2,1,0,0.5]
        return dot_product(feature, weight)

    def minimax(self, state, depth_run, depth_ori, color):
        if depth_run == 0 or self.terminal(state, color):
            return [self.heuristic(state, depth_ori), []]
        if color == 1:
            best_value = -INF
            valid_moves = self.move_gen(state,color)
            best_move = valid_moves[0]
            for move in valid_moves:
                result = self.minimax(doit(move, state), depth_run - 1, depth_ori, -color)
                move_value = result[0]
                # best_value = max(best_value, move_value)
                if (move_value > best_value):
                    best_move = move
                    best_value = move_value
            return [best_value, best_move]
        else:
            best_value = INF
            valid_moves = self.move_gen(state, -color)
            best_move = valid_moves[0]
            for move in valid_moves:
                result = self.minimax(doit(move, state), depth_run - 1, depth_ori, color)
                move_value = result[0]
                # best_value = min(best_value, move_value)
                if (move_value < best_value):
                    best_move = move
                    best_value = move_value
            return [best_value, best_move]

    def negamax(self, state, depth_run, depth_ori, color):
        if depth_run == 0 or self.terminal(state, color):
            return [color * self.heuristic(state, depth_ori), []]
        best_value = -INF
        valid_moves = self.move_gen(state, color)
        best_move = valid_moves[0]
        for move in valid_moves:
            result = self.negamax(doit(move, state), depth_run - 1, depth_ori, -color)
            move_value = -result[0]
            # best_value = max(best_value, move_value)
            if move_value > best_value:
                best_move = move
                best_value = move_value
        return [best_value, best_move]

    def negamax_alpha_beta(self, state, depth_run, depth_ori, alpha, beta, color):
        if depth_run == 0 or self.terminal(state, color):
            return [color * self.heuristic(state, depth_ori), []]
        best_value = -INF
        valid_moves = self.move_gen(state, color)
        best_move = valid_moves[0]
        # order later
        for move in valid_moves:
            state_moved = self.negamax_alpha_beta(doit(move, state), depth_run - 1, depth_ori, -beta, -alpha, -color)
            move_value = -state_moved[0]
            if move_value > best_value:
                best_value = move_value
                best_move = move
            alpha = max(alpha, move_value)
            if alpha >= beta:
                break
        return [best_value, best_move]

    def negamax_alpha_beta_timer(self, state, depth_run, depth_ori, alpha, beta, color, time_start):
        if time.time() - time_start > 2.9:
            return OVER_TIME
        if depth_run == 0 or self.terminal(state, color):
            return [color * self.heuristic(state, depth_ori), []]
        best_value = -INF
        valid_moves = self.move_gen(state, color)
        best_move = valid_moves[0]
        # order later
        for move in valid_moves:
            state_moved = self.negamax_alpha_beta_timer(doit(move, state), depth_run - 1, depth_ori,
                                                        -beta, -alpha, -color, time_start)
            if state_moved == OVER_TIME:
                return OVER_TIME
            move_value = -state_moved[0]
            if move_value > best_value and move != []:
                best_value = move_value
                best_move = move
            alpha = max(alpha, move_value)
            if alpha >= beta:
                break
        return [best_value, best_move]

    def negamax_alpha_beta_interative_depending(self, state, depth_max, alpha, beta, color, time_start):
        res = []
        for depth in range(1, depth_max+1):
            current_depth_value = self.negamax_alpha_beta_timer(state, depth, depth, alpha, beta, color, time_start)
            if current_depth_value != OVER_TIME:
                res += [current_depth_value]
            else:
                break
        print("Stop at depth: {}.\n".format(depth))
        if self.heuristic_fun == 3:
            if len(res) % 2 == 0:
                return res[-2]
            else:
                return res[-1]
        else:
            return res[-1]

    # Student MUST implement this function
    # The return value should be a move that is denoted by a list of tuples
    # fine is good
    def nextMove(self, state):
        if self.strategy == 1:
            estimate = self.negamax_alpha_beta(state, 5, 5, -INF, INF, 1)
        elif self.strategy == 2:
            estimate = self.negamax_alpha_beta_interative_depending(state, INF, -INF, INF, 1, time.time())
        else:
            estimate = self.minimax(state, 5, 5, 1)
        return estimate[1]