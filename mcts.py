from math import sqrt, log,e
import random
import copy
from randplay import *

class State:
    def __init__(self,  grid, player, row, col, l_row, l_col):
        self.grid = grid
        self.piece = player
        self.values = 0
        self.visitNum = 0
        self.parent = 0
        self.children = []
        self.row = row
        self.position = (row, col)
        self.col = col
        self.l_row = l_row
        self.l_col = l_col
        self.index = 0              #index in the tree_policy
        self.explored = {}
        
        pass

class MCTS:
    #while chess pice put on (row, col), now it is 'b' turn 
    def __init__(self, grid,player, row, col,l_row , l_col ):
        # print "\n"
        # print "call MCTS"
        self.grid = grid
        self.grid_size = len(grid)
        self.piece = player
        self.opt_piece = 'b'
        if self.piece == 'b':
            self.opt_piece = 'w'
        else:
            self.opt_piece = 'b'
        self.row = row
        self.col = col
        self.l_row = l_row
        self.l_col = l_col
        self.tree = [] 
        
        self.tree_index = 0
        # self.explored = {}
        
    def uct_search(self):
        #init root state
        root = State(self.grid,self.piece, self.row, self.col, self.l_row, self.l_col )
        if self.piece == 'b':
            root.grid[self.row][self.col] = 'w'
        else:
            root.grid[self.row][self.col] = 'b'
        self.tree.append(root)
        root.explored[self.row, self.col] = 1 #explored itself 
        root.index = self.tree_index
        self.tree_index += 1
        
        # if root.l_row != -1 and root.l_col != 0:
            # if self.first_step(root) != (-1, -1):
                # r,c = self.first_step(root)
                # return State(self.grid, self.piece, r, c, -1, -1)
        
        i = 0
        while (i < 4000):
            # print "the ", i, " iteration"
            
            child = self.tree_policy(root)
            # print "uct_search:  after tree_policy"            
            reward = self.default_policy(child)
            
            self.backup(child, reward)
            
            i += 1
        # for i in range (len(self.tree)):
            # print "position: ", self.tree[i].position, "parent: ",self.tree[i].parent, "values: ",self.tree[i].values, "visitnum: ", self.tree[i].visitNum
        
        return self.best_child(root)
            
        
    def tree_policy(self, state):
        temp = state
        # print "tree_policy: ", state.position
        while True:
            if not self.is_fullexplore(temp):
                t1 = self.expand(temp)
                return t1
                # return self.expand(temp)
            else:
                # print "tree_policy: after expand----"
                
                temp = self.best_child(temp)
                if self.is_terminal(temp):
                    return temp
                # print "tree_policy: temp is ", temp.position, "index is ", temp.index, "parent is ", temp.parent
                
        
        
    #not check the current step, we need check the previous step (take turn chess game)     
    def is_fullexplore (self,state):
        #special condition the first step on the board
        if state.l_row == -1 and state.l_col == -1:
            left = state.col - 1
            right = state.col + 1
            up = state.row - 1
            down = state.row + 1
            while left < 0:
                left += 1
            while right >= self.grid_size:
                right -= 1
            while up < 0:
                up += 1
            while down  >= self.grid_size:
                down -= 1
            j = left
            i = up    
            while i <= down:
                j = left
                while j <= right:
                    if state.grid[i][j] == '.' and (i, j) not in state.explored:
                        return False
                
                    j += 1
                i += 1
            return True
        
        left = state.l_col - 1
        right = state.l_col + 1
        up = state.l_row - 1
        down = state.l_row + 1
        while left < 0:
            left += 1
        while right >= self.grid_size:
            right -= 1
        while up < 0:
            up += 1
        while down  >= self.grid_size:
            down -= 1
        j = left
        i = up    
        while i <= down:
            j = left
            while j <= right:
                if state.grid[i][j] == '.' and (i, j) not in state.explored:
                    return False
                
                j += 1
            i += 1
        
        # if state.piece == self.piece:
            # r, c = self.check_o_side(state)
            # if r != -1 and c != -1:  #valid position
                # return False
        
        return True
    
    #check other side of the line of chess piece
    #now just test 4 direction 
    def check_o_side (self, state):
        length = {}
        #up
        up = state.l_row 
        t = 1                 #the length of same color on the direct
        while up - 1 >= 0 and state.grid[up][state.l_col] == state.piece:
            t += 1 
            up -= 1
        if up >= 0 and state.grid[up][state.l_col] == '.' and (up, state.l_col) not in state.explored:     #not state.piece & not edge
            length[up, state.l_col] = t   
        
        #down
        down = state.l_row
        t = 1
        while down + 1 < self.grid_size and state.grid[down][state.l_col] == state.piece:
            t += 1 
            down += 1
        if down < self.grid_size and state.grid[down][state.l_col] == '.' and (down, state.l_col) not in state.explored:
            length[down, state.l_col] = t
        
        #left
        left = state.l_col
        t = 1
        while left - 1 >= 0 and  state.grid[state.l_row][left] == state.piece:
            t += 1
            left -= 1
        if left >= 0 and state.grid[state.l_row][left] == '.' and (state.l_row, left) not in state.explored:
            length[state.l_row, left] = t
        
        #right
        right = state.l_col
        t = 1
        while left + 1 < self.grid_size and state.grid[state.l_row][right] == state.piece:
            t += 1
            right += 1
        if right < self.grid_size and state.grid[state.l_row][right] == '.' and (state.l_row, right) not in state.explored:
            length[state.l_row, right] = t
            
        #up and right
        right = state.l_col
        up = state.l_row
        t = 1
        while (up - 1 >= 0 and left + 1 < self.grid_size) and state.grid[up][right] == state.piece:
            t += 1
            right += 1
            up -= 1
        if up >= 0 and right < self.grid_size and state.grid[up][right] == '.' and (up, right) not in state.explored:
            length[up, right] = t
            
        
            
        #down and right
        right = state.l_col
        down = state.l_row
        t = 1
        while down + 1 < self.grid_size and left + 1 < self.grid_size and state.grid[down][right] == state.piece:
            t += 1
            right += 1
            down += 1
        if down < self.grid_size and right < self.grid_size and state.grid[down][right] == '.' and (down, right) not in state.explored:
            length[down, right] = t
            
        #left and up
        left = state.l_col
        up = state.l_row
        t = 1
        while up - 1 >= 0 and left - 1 >= 0 and  state.grid[up][left] == state.piece:
            t += 1
            left -= 1
            up -= 1
        if up >=0 and left >= 0 and state.grid[up][left] == '.' and (up, left) not in state.explored:
            length[up, left] = t
            
        #left and down
        left = state.l_col
        down = state.l_row
        t = 1
        while down + 1 < self.grid_size and left - 1 >= 0 and  state.grid[down][left] == state.piece:
            t += 1
            left -= 1
            down += 1
        if left >= 0 and down < self.grid_size and state.grid[down][left] == '.' and (down, left) not in state.explored:
            length[down, left] = t
            
        t = 0
        r = -1
        c = -1
        for i in length:
            if t <= length[i]:
                t = length[i]
                r,c = i 
        return (r, c)
            
    def expand(self, state):
        
        # print "~~~~~~~~~~expand:  func begin , state is  ",state.position, state.index
        # for i in range (len(self.tree)):
            # print "position: ", self.tree[i].position, "index: ", self.tree[i].index, "parent: ",self.tree[i].parent, "values: ",self.tree[i].values, "visitnum: ", self.tree[i].visitNum
        if state.piece == 'b':
            opt_piece = 'w'
        else:
            opt_piece = 'b'
        # print "l_r:", state.l_row,"l_c:", state.l_col
        #the root
        if state.l_row == -1 and state.l_col == -1:
            left = state.col - 1
            right = state.col + 1
            up = state.row - 1
            down = state.row + 1
            while left < 0:
                left += 1
            while right >= self.grid_size:
                right -= 1
            while up < 0:
                up += 1
            while down  >= self.grid_size:
                down -= 1
            j = left
            i = up    
            while i <= down:
                j = left
                while j <= right:
                    if state.grid[i][j] == '.' and (i, j) not in state.explored:
                        state.explored[(i, j)] = 1
                    
                        node = State(copy.deepcopy(state.grid), opt_piece, i, j, state.row, state.col)
                        # print "expand 1:  find a position", node.position
                        node.grid[i][j] = opt_piece 
                        # node.l_row = state.row
                        # node.l_col = state.col
                        self.tree.append(node)
                        node.index = self.tree_index
                        self.tree_index += 1
                        node.parent = state.index
                        state.children.append(node.index)
                        #node.path = state.path.copy()
                        #node.path[i,j] = 1
                        return node
                    
                    j += 1
                i += 1
            
        
        # print ("not first step")
        left = state.l_col - 1
        right = state.l_col + 1
        up = state.l_row - 1
        down = state.l_row + 1
        while left < 0:
            left += 1
        while right >= self.grid_size:
            right -= 1
        while up < 0:
            up += 1
        while down  >= self.grid_size:
            down -= 1
        j = left
        i = up    
        while i <= down:
            j = left
            while j <= right:
                if state.grid[i][j] == '.' and (i, j) not in state.explored:
                    state.explored[(i, j)] = 1
                    
                    node = State(copy.deepcopy(state.grid), opt_piece, i, j,state.row, state.col)
                    # print "expand 2:  find a position", node.position
                    state.grid[i][j] = opt_piece 
                    # node.l_row = state.row
                    # node.l_col = state.col
                    self.tree.append(node)
                    node.index = self.tree_index
                    self.tree_index += 1
                    node.parent = state.index
                    state.children.append(node.index)
                    #node.path = state.path.copy()
                    #node.path[i,j] = 1
                    return node
                
                j += 1
            i += 1
        

        
    def best_child(self, state):
        
        index = 0
        best_chess = self.tree[state.children[index]]
        while index < len(state.children):
            best_q = best_chess.values
            best_n = best_chess.visitNum
            # print ("current v, Q(v)", best_q, "N(v):", best_n)
            parent_n = state.visitNum
            # print ("parent N: ", parent_n)
            # print("parent_nvisit num is ", state.visitNum)
            com_q = self.tree[state.children[index]].values
            com_n = self.tree[state.children[index]].visitNum
            # print ("next Q(v): ", com_q, "N(v): ", com_n)
            if (best_q * 1.0 / best_n + 2*sqrt(2.0 * log(parent_n, e)/ best_n)) < (com_q * 1.0 / com_n +  2*sqrt(2.0 * log(parent_n, e)/ com_n)):
                best_chess = self.tree[state.children[index]]
            index += 1
            # print com_q * 1.0 / com_n +  5*sqrt(2.0 * log(parent_n, e)/ com_n)
        return best_chess        
                
    def is_terminal(self, state):
        r = state.l_row
        c = state.l_col
                
       
        if len(state.children) == 0 :
            return True
        return False 
        
    def default_policy(self, state):
        random_grid = copy.deepcopy(state)
        # print "default policy: ", random_grid.row, random_grid.col
        
       
                
        while True:
            if random_grid.piece == self.piece:
                # print "default_policy: in defand ~~"
                r, c = self.attack_player(random_grid, random_grid.row, random_grid.col)
                # if (r,c) is not None:
                random_grid.grid[r][c] = self.piece
                # else:
                    # print "it is none"
                random_grid.piece = self.opt_piece
                random_grid.l_row = random_grid.row
                random_grid.l_col = random_grid.col
                
                random_grid.row = r
                random_grid.col = c
                # print "defen: ", random_grid.row, random_grid.col, "~~"
                if self.check_win(random_grid, r, c):
                    return 1
            if random_grid.piece == self.opt_piece:
                # print "default_policy: in attack @@"
                # r, c = self.defend_player(random_grid, random_grid.row, random_grid.col)
                player1  = Randplay(self.grid, self.piece)
                r, c = player1.make_move()
                # if (r,c) is not None:
                random_grid.grid[r][c] = self.opt_piece
                # else:
                    # print "it is none"
                random_grid.piece = self.piece
                random_grid.l_row = random_grid.row
                random_grid.l_col = random_grid.col
                random_grid.row = r
                random_grid.col = c
                # print "attack: ", random_grid.row, random_grid.col, "@@"
                if self.check_win(random_grid, r, c):
                    return 0
                    
                    

                    
    # def first_step (self, state):
        r = state.row
        c = state.col 
        l_r = state.l_row
        l_c = state.l_col
        first = state
         
        # attack 4
        l_left =l_c - 1
        l_right = l_c + 1
        l_up = l_r- 1
        l_down = l_r + 1
        while l_left < 0:
            l_left += 1
        while l_right >= self.grid_size:
            l_right -= 1
        while l_up < 0:
            l_up += 1
        while l_down  >= self.grid_size:
            l_down -= 1 
        
        j = l_left
        i = l_up    
        while i <= l_down:
            j = l_left
            while j <= l_right:
                if state.grid[i][j] == state.piece:
                    if self.check_line_by_position_4(first, i, j) != (-1, -1):
                        return self.check_line_by_position_4(first, i, j)
                    
                j += 1
            i += 1
        
        #defend 4
        if self.check_line_by_position_4(first, r, c) != (-1, -1):
            return self.check_line_by_position_4(first, r, c)
        
        #attack two sizes 3
              
        
            
        j = l_left
        i = l_up    
        while i <= l_down:
            j = l_left
            while j <= l_right:
                if state.grid[i][j] == state.piece:
                    if self.check_line_by_position_3(first, i, j) != (-1, -1):
                        return self.check_line_by_position_3(first, i, j)
                    
                j += 1
            i += 1
        
        #defend 3
        if self.check_line_by_position_3(first, r, c) != (-1, -1):
            return self.check_line_by_position_3(first, r, c)
        return (-1, -1)
            
    def check_line_by_position_3 (self, state, r, c):
        check = state
        n_count = self.get_continuous_count(check.grid, r, c, -1, 0)
        s_count = self.get_continuous_count(check.grid, r, c, 1, 0)
        e_count = self.get_continuous_count(check.grid, r, c, 0, 1)
        w_count = self.get_continuous_count(check.grid, r, c, 0, -1)
        se_count = self.get_continuous_count(check.grid, r, c, 1, 1)
        nw_count = self.get_continuous_count(check.grid, r, c, -1, -1)
        ne_count = self.get_continuous_count(check.grid,r, c, -1, 1)
        sw_count = self.get_continuous_count(check.grid, r, c, 1, -1)
        
        # two side line 3
        if n_count + s_count + 1 == 3:
            if r - n_count - 1 >= 0 and check.grid[r - n_count - 1][c] == '.':
                if r + s_count + 1 < self.grid_size and check.grid[r + s_count + 1][c] == '.':
                    if r + s_count + 2 < self.grid_size and check.grid[r + s_count + 2][c] == '.':
                        return (r + s_count + 1, c)
                    if r - n_count - 2 >= 0 and check.grid[r - n_count - 2][c] == '.':
                        return (r - n_count - 1, c)
        
        # e_w line >= 3
        if e_count + w_count + 1 == 3:
            if c - w_count - 1 >= 0  and check.grid[r][c - w_count - 1] == '.':
                if c + e_count + 1 < self.grid_size and check.grid[r][c + e_count + 1] == '.':
                    if c + e_count + 2 < self.grid_size and check.grid[r][c + e_count + 2] == '.':
                        return (r, c + e_count +1)
                    if c - w_count - 2 >= 0  and check.grid[r][c - w_count - 2] == '.':
                        return (r, c - w_count - 1)
          
        # nw - se
        if se_count + nw_count + 1 == 3:
            if r + se_count + 1 < self.grid_size and c + se_count + 1 < self.grid_size and check.grid[r + se_count + 1][c + se_count + 1] == '.':
                if r - nw_count - 1 >= 0 and c - nw_count - 1 >= 0 and check.grid[r - nw_count - 1][c - nw_count - 1] == '.':
                    if r - nw_count - 2 >= 0 and c - nw_count - 2 >= 0 and check.grid[r - nw_count - 2][c - nw_count - 2] == '.':
                        return (r - nw_count - 1, c - nw_count - 1)
                    if r + se_count + 2 < self.grid_size and c + se_count + 2 < self.grid_size and check.grid[r + se_count + 2][c + se_count + 2] == '.':
                        return (r + se_count + 1, c + se_count + 1)
               
        if ne_count + sw_count + 1 == 3:
            if r - ne_count - 1 >= 0 and c + ne_count + 1 < self.grid_size and check.grid[r - ne_count - 1][c + ne_count + 1] == '.':
                if r + sw_count + 1 < self.grid_size and c - sw_count - 1 >= 0 and check.grid[r + sw_count + 1][c - sw_count - 1] == '.':
                    if r + sw_count + 2 < self.grid_size and c - sw_count - 2 >= 0 and check.grid[r + sw_count + 2][c - sw_count - 2] == '.':
                        return (r + sw_count + 1, c - sw_count - 1)
                    if r - ne_count - 2 >= 0 and c + ne_count + 2 < self.grid_size and check.grid[r - ne_count - 2][c + ne_count + 2] == '.':
                        return (r - ne_count - 1, c + ne_count + 1)
        return (-1, -1)
            
    def check_line_by_position_4 (self, state, r, c):
        check = state
        n_count = self.get_continuous_count(check.grid, r, c, -1, 0)
        s_count = self.get_continuous_count(check.grid, r, c, 1, 0)
        e_count = self.get_continuous_count(check.grid, r, c, 0, 1)
        w_count = self.get_continuous_count(check.grid, r, c, 0, -1)
        se_count = self.get_continuous_count(check.grid, r, c, 1, 1)
        nw_count = self.get_continuous_count(check.grid, r, c, -1, -1)
        ne_count = self.get_continuous_count(check.grid,r, c, -1, 1)
        sw_count = self.get_continuous_count(check.grid, r, c, 1, -1)
        
        # defend: line 4
        if n_count + s_count + 1 == 4:
            if r - n_count - 1 >= 0 and check.grid[r - n_count - 1][c] == '.':
                return (r - n_count - 1, c)
            elif r + s_count + 1 < self.grid_size and check.grid[r + s_count + 1][c] == '.':
                return (r + s_count + 1, c)
        
            # e_w 
        if e_count + w_count + 1 == 4:
            if c - w_count - 1 >= 0  and check.grid[r][c - w_count - 1] == '.':
                return (r, c - w_count - 1);
            elif c + e_count + 1 < self.grid_size and check.grid[r][c + e_count + 1] == '.':
                return (r, c + e_count + 1)
             
        # nw - se
        if se_count + nw_count + 1 == 4:
            if r + se_count + 1 < self.grid_size and c + se_count + 1 < self.grid_size and check.grid[r + se_count + 1][c + se_count + 1] == '.':
                return (r + se_count + 1, c + se_count + 1)
            elif r - nw_count - 1 >= 0 and c - nw_count - 1 >= 0 and check.grid[r - nw_count - 1][c - nw_count - 1] == '.':
                return (r - nw_count - 1, c - nw_count - 1)
                
        if ne_count + sw_count + 1 == 4:
            if r - ne_count - 1 >= 0 and c + ne_count + 1 < self.grid_size and check.grid[r - ne_count - 1][c + ne_count + 1] == '.':
                return (r - ne_count - 1, c + ne_count + 1)
            elif r + sw_count + 1 < self.grid_size and c - sw_count - 1 >= 0 and check.grid[r + sw_count + 1][c - sw_count - 1] == '.':
                return (r + sw_count + 1, c - sw_count - 1)
        return (-1, -1)
    
    
    def attack_player (self, state, r, c):
        # print "attack_player"
        l_r = state.l_row
        l_c = state.l_col
        # print "l_r: ", l_r, "l_c: ", l_c
        # print "r: ", r, "c: ", c
        attack = state
        
        
        
        #current step effect
        n_count = self.get_continuous_count(attack.grid, r, c, -1, 0)
        s_count = self.get_continuous_count(attack.grid, r, c, 1, 0)
        e_count = self.get_continuous_count(attack.grid, r, c, 0, 1)
        w_count = self.get_continuous_count(attack.grid, r, c, 0, -1)
        se_count = self.get_continuous_count(attack.grid, r, c, 1, 1)
        nw_count = self.get_continuous_count(attack.grid, r, c, -1, -1)
        ne_count = self.get_continuous_count(attack.grid,r, c, -1, 1)
        sw_count = self.get_continuous_count(attack.grid, r, c, 1, -1)
        
        #last step effect
        l_n_count = self.get_continuous_count(attack.grid, l_r, l_c, -1, 0)
        l_s_count = self.get_continuous_count(attack.grid, l_r, l_c, 1, 0)
        l_e_count = self.get_continuous_count(attack.grid, l_r, l_c, 0, 1)
        l_w_count = self.get_continuous_count(attack.grid, l_r, l_c, 0, -1)
        l_se_count = self.get_continuous_count(attack.grid, l_r, l_c, 1, 1)
        l_nw_count = self.get_continuous_count(attack.grid, l_r, l_c, -1, -1)
        l_ne_count = self.get_continuous_count(attack.grid,l_r, l_c, -1, 1)
        l_sw_count = self.get_continuous_count(attack.grid, l_r, l_c, 1, -1)
        
        
        #attack :line 4
     
        if l_n_count + l_s_count + 1 == 4:
            if l_r - l_n_count - 1 >= 0 and attack.grid[l_r - l_n_count - 1][l_c] == '.':
                return (l_r - l_n_count - 1, l_c)
            elif l_r + l_s_count + 1 < self.grid_size and attack.grid[l_r + l_s_count + 1][l_c] == '.':
                return (l_r + l_s_count + 1, l_c)
            
        # e_w 
        if l_e_count + l_w_count + 1 == 4:
            if l_c - l_w_count - 1 >= 0  and attack.grid[l_r][l_c - l_w_count - 1] == '.':
                return (l_r, l_c - l_w_count - 1);
            elif l_c + l_e_count + 1 < self.grid_size and attack.grid[l_r][l_c + l_e_count + 1] == '.':
                return (l_r, l_c + l_e_count + 1)
             
        # nw - se
        if l_se_count + l_nw_count + 1 == 4:
            if l_r + l_se_count + 1 < self.grid_size and l_c + l_se_count + 1 < self.grid_size and attack.grid[l_r + l_se_count + 1][l_c + l_se_count + 1] == '.':
                return (l_r + l_se_count + 1, l_c + l_se_count + 1)
            elif l_r - l_nw_count - 1 >= 0 and l_c - l_nw_count - 1 >= 0 and attack.grid[l_r - l_nw_count - 1][l_c - l_nw_count - 1] == '.':
                return (l_r - l_nw_count - 1, l_c - l_nw_count - 1)
                
        if l_ne_count + l_sw_count + 1 == 4:
            if l_r - l_ne_count - 1 >= 0 and l_c + l_ne_count + 1 < self.grid_size and attack.grid[l_r - l_ne_count - 1][l_c + l_ne_count + 1] == '.':
                return (l_r - l_ne_count - 1, l_c + l_ne_count + 1)
            elif l_r + l_sw_count + 1 < self.grid_size and l_c - l_sw_count - 1 >= 0 and attack.grid[l_r + l_sw_count + 1][l_c - l_sw_count - 1] == '.':
                return (l_r + l_sw_count + 1, l_c - l_sw_count - 1)
        
        
        # defend: line 4
        if n_count + s_count + 1 == 4:
            if r - n_count - 1 >= 0 and attack.grid[r - n_count - 1][c] == '.':
                return (r - n_count - 1, c)
            elif r + s_count + 1 < self.grid_size and attack.grid[r + s_count + 1][c] == '.':
                return (r + s_count + 1, c)
        
            # e_w 
        if e_count + w_count + 1 == 4:
            if c - w_count - 1 >= 0  and attack.grid[r][c - w_count - 1] == '.':
                return (r, c - w_count - 1);
            elif c + e_count + 1 < self.grid_size and attack.grid[r][c + e_count + 1] == '.':
                return (r, c + e_count + 1)
             
        # nw - se
        if se_count + nw_count + 1 == 4:
            if r + se_count + 1 < self.grid_size and c + se_count + 1 < self.grid_size and attack.grid[r + se_count + 1][c + se_count + 1] == '.':
                return (r + se_count + 1, c + se_count + 1)
            elif r - nw_count - 1 >= 0 and c - nw_count - 1 >= 0 and attack.grid[r - nw_count - 1][c - nw_count - 1] == '.':
                return (r - nw_count - 1, c - nw_count - 1)
                
        if ne_count + sw_count + 1 == 4:
            if r - ne_count - 1 >= 0 and c + ne_count + 1 < self.grid_size and attack.grid[r - ne_count - 1][c + ne_count + 1] == '.':
                return (r - ne_count - 1, c + ne_count + 1)
            elif r + sw_count + 1 < self.grid_size and c - sw_count - 1 >= 0 and attack.grid[r + sw_count + 1][c - sw_count - 1] == '.':
                return (r + sw_count + 1, c - sw_count - 1)
        
        #attack two side line 3
        # two side line 3
        if l_n_count + l_s_count + 1 == 3:
            if l_r - l_n_count - 1 >= 0 and attack.grid[l_r - l_n_count - 1][l_c] == '.':
                if l_r + l_s_count + 1 < self.grid_size and attack.grid[l_r + l_s_count + 1][l_c] == '.' and l_r + l_s_count + 2 <  self.grid_size and attack.grid[l_r + l_s_count + 2][l_c] == '.':
                    return (l_r + l_s_count + 1, l_c)
                elif l_r - l_n_count - 2 >= 0 and attack.grid[l_r - l_n_count - 2][l_c] == '.':
                    return (l_r - l_n_count - 1, l_c)
        
        # e_w line >= 3
        if l_e_count + l_w_count + 1 == 3:
            if l_c - l_w_count - 1 >= 0  and attack.grid[l_r][l_c - l_w_count - 1] == '.':
                if l_c + l_e_count + 1 < self.grid_size and attack.grid[l_r][l_c + l_e_count + 1] == '.' and l_c + l_e_count + 2 < self.grid_size and attack.grid[l_r][l_c + l_e_count + 2] == '.':
                    return (l_r, l_c + l_e_count + 1)
                elif l_c - l_w_count - 2 >= 0  and attack.grid[l_r][l_c - l_w_count - 2] == '.':
                    return (l_r , l_c - l_w_count - 1)
             
        # nw - se
        if l_se_count + l_nw_count + 1 == 3:
            if l_r + l_se_count + 1 < self.grid_size and l_c + l_se_count + 1 < self.grid_size and attack.grid[l_r + l_se_count + 1][l_c + l_se_count + 1] == '.':
                if l_r - l_nw_count - 1 >= 0 and l_c - l_nw_count - 1 >= 0 and attack.grid[l_r - l_nw_count - 1][l_c - l_nw_count - 1] == '.' and l_r - l_nw_count - 2 >= 0 and l_c - l_nw_count - 2 >= 0 and attack.grid[l_r - l_nw_count - 2][l_c - l_nw_count - 2] == '.':
                    return (l_r - l_nw_count - 1, l_c - l_nw_count - 1)
                elif l_r + l_se_count + 2 < self.grid_size and l_c + l_se_count + 2 < self.grid_size and attack.grid[l_r + l_se_count + 2][l_c + l_se_count + 2] == '.':
                    return (l_r + l_se_count + 1, l_c + l_se_count + 1)
                
        if l_ne_count + l_sw_count + 1 == 3:
            if l_r - l_ne_count - 1 >= 0 and l_c + l_ne_count + 1 < self.grid_size and attack.grid[l_r - l_ne_count - 1][l_c + l_ne_count + 1] == '.':
                if l_r + l_sw_count + 1 < self.grid_size and l_c - l_sw_count - 1 >= 0 and attack.grid[l_r + l_sw_count + 1][l_c - l_sw_count - 1] == '.' and l_r + l_sw_count + 2 < self.grid_size and l_c - l_sw_count - 2 >= 0 and attack.grid[l_r + l_sw_count + 2][l_c - l_sw_count - 2] == '.':
                    return (l_r + l_sw_count + 1, l_c - l_sw_count - 1)
                elif l_r - l_ne_count - 1 >= 0 and l_c + l_ne_count + 1 < self.grid_size and attack.grid[l_r - l_ne_count - 1][l_c + l_ne_count + 1] == '.':
                    return (l_r - l_ne_count - 1, l_c + l_ne_count + 1)
        
        
        #defend  two side line 3
                
        # two side line 3
        if n_count + s_count + 1 == 3:
            if r - n_count - 1 >= 0 and attack.grid[r - n_count - 1][c] == '.':
                if r + s_count + 1 < self.grid_size and attack.grid[r + s_count + 1][c] == '.'  :
                    if r - n_count - 2 >= 0 and attack.grid[r - n_count - 2][c] == '.':
                        return (r - n_count - 1, c)
                    if r + s_count + 2 < self.grid_size and attack.grid[r + s_count + 2][c] == '.' :
                        return (r + s_count + 1, c)
        # e_w line >= 3
        if e_count + w_count + 1 == 3:
            if c - w_count - 1 >= 0  and attack.grid[r][c - w_count - 1] == '.':
                if c + e_count + 1 < self.grid_size and attack.grid[r][c + e_count + 1] == '.':
                    if c - w_count - 2 >= 0  and attack.grid[r][c - w_count - 2] == '.':
                        return (r, c - w_count - 1)
                        
                    elif c + e_count + 2 < self.grid_size and attack.grid[r][c + e_count + 2] == '.':
                        return (r, c + e_count + 1)
                        
          
        # nw - se
        if se_count + nw_count + 1 == 3:
            if r + se_count + 1 < self.grid_size and c + se_count + 1 < self.grid_size and attack.grid[r + se_count + 1][c + se_count + 1] == '.':
                if r - nw_count - 1 >= 0 and c - nw_count - 1 >= 0 and attack.grid[r - nw_count - 1][c - nw_count - 1] == '.':
                    if r + se_count + 2 < self.grid_size and c + se_count + 2 < self.grid_size and attack.grid[r + se_count + 2][c + se_count + 2] == '.':
                        return (r + se_count + 1, c + se_count + 1)
                        
                    if r - nw_count - 2 >= 0 and c - nw_count - 2 >= 0 and attack.grid[r - nw_count - 2][c - nw_count - 2] == '.':
                        return (r - nw_count - 1, c - nw_count - 1)
               
        if ne_count + sw_count + 1 == 3:
            if r - ne_count - 1 >= 0 and c + ne_count + 1 < self.grid_size and attack.grid[r - ne_count - 1][c + ne_count + 1] == '.':
                if r + sw_count + 1 < self.grid_size and c - sw_count - 1 >= 0 and attack.grid[r + sw_count + 1][c - sw_count - 1] == '.':
                    if r - ne_count - 2 >= 0 and c + ne_count + 2 < self.grid_size and attack.grid[r - ne_count - 2][c + ne_count + 2] == '.':
                        return (r - ne_count - 1, c + ne_count + 1)
                        
                    if r + sw_count + 2 < self.grid_size and c - sw_count - 2 >= 0 and attack.grid[r + sw_count + 2][c - sw_count - 2] == '.':
                        return (r + sw_count + 1, c - sw_count - 1)
                     
        
        # print "attack_player: after priority"  
        size = 2
        while size <= 18:
            
            # print "attack func size is ",size
            left = attack.col - size
            right = attack.col + size
            up = attack.row - size
            down = attack.row + size
            while left < 0:
                left += 1
            while right >= self.grid_size:
                right -= 1
            while up < 0:
                up += 1
            while down  >= self.grid_size:
                down -= 1
            j = left
            i = up
         # print('best_child: size of children is  0', state.position)
            counter = 0
            while i <= down:
                j = left
                while j <= right:
                    if attack.grid[i][j] == '.':
                        counter += 1
                    j += 1
                i += 1
            
            if counter == 0:
                size += 1
                
            # while True:
                # r_r = random.randint(0,18);
                # r_c = random.randint(0,18);
                # if attack.grid[r_r][r_c] == '.':
                    # return (r_r,r_c)
            # player = Randplay(attack.grid, attack.piece)
            # ret_r, ret_c = player.make_move();
            else:
                m = random.randint(0, counter - 1)
                j = left
                i = up
            # print('best_child: size of children is  0', state.position)
                while i <= down:
                    j = left
                    while j <= right:
                        if attack.grid[i][j] == '.' and m == 0:
                            return (i, j)
                        if attack.grid[i][j] == '.' and m!= 0:
                            m -= 1
                        
                        j += 1
                    i += 1
        
            
    def backup (self, state, reward):
        cur = state
        if reward == 1:
            n_reward = 0
        else:
            n_reward = 1
        # print('backup: while')
        while cur.index != 0:
            
            # print('backup:  current', cur.position,'Q is ', cur.values, 'N is ', cur.visitNum, 'parent index', cur.parent)
            if cur.piece == self.piece:
                cur.values += reward
            else:
                cur.values += n_reward
            cur.visitNum += 1
            cur = self.tree[cur.parent]
            
        #if it was root
        cur.visitNum += 1
        cur.values += reward
        
        
    # def defend_player(self, state, r, c):
        # l_r = state.l_row
        # l_c = state.l_col
        # defend = state
        # n_count = self.get_continuous_count(defend.grid, r, c, -1, 0)
        # s_count = self.get_continuous_count(defend.grid, r, c, 1, 0)
        # e_count = self.get_continuous_count(defend.grid, r, c, 0, 1)
        # w_count = self.get_continuous_count(defend.grid, r, c, 0, -1)
        # se_count = self.get_continuous_count(defend.grid, r, c, 1, 1)
        # nw_count = self.get_continuous_count(defend.grid, r, c, -1, -1)
        # ne_count = self.get_continuous_count(defend.grid,r, c, -1, 1)
        # sw_count = self.get_continuous_count(defend.grid, r, c, 1, -1)
        
        # if n_count + s_count + 1 >= 3:
            # if r - n_count - 1 >= 0 and defend.grid[r - n_count - 1][c] == '.':
                # return (r - n_count - 1, c)
            # elif r + s_count + 1 < self.grid_size and defend.grid[r + s_count + 1][c] == '.':
                # return (r + s_count + 1, c)
        
        # if e_count + w_count + 1 >= 3:
            # if c - w_count - 1 >= 0  and defend.grid[r][c - w_count - 1] == '.':
                # return (r, c - w_count - 1);
            # elif c + e_count + 1 < self.grid_size and defend.grid[r][c + e_count + 1] == '.':
                # return (r, c + e_count + 1)
             
        # if se_count + nw_count + 1 >= 3:
            # if r + se_count + 1 < self.grid_size and c + se_count + 1 < self.grid_size and defend.grid[r + se_count + 1][c + se_count + 1] == '.':
                # return (r + se_count + 1, c + se_count + 1)
            # elif r - nw_count - 1 >= 0 and c - nw_count - 1 >= 0 and defend.grid[r - nw_count - 1][c - nw_count - 1] == '.':
                # return (r - nw_count - 1, c - nw_count - 1)
                
        # if ne_count + sw_count + 1 >= 3:
            # if r - ne_count - 1 >= 0 and c + ne_count + 1 < self.grid_size and defend.grid[r - ne_count - 1][c + ne_count + 1] == '.':
                # return (r - ne_count - 1, c + ne_count + 1)
            # elif r + sw_count + 1 < self.grid_size and c - sw_count - 1 >= 0 and defend.grid[r + sw_count + 1][c - sw_count - 1] == '.':
                # return (r + sw_count + 1, c - sw_count - 1)
        
        # size = 2
        # while size <= 18:
            # left = defend.col - size
            # right = defend.col + size
            # up = defend.row - size
            # down = defend.row + size
            # while left < 0:
                # left += 1
            # while right >= self.grid_size:
                # right -= 1
            # while up < 0:
                # up += 1
            # while down  >= self.grid_size:
                # down -= 1
            # j = left
            # i = up
            # counter = 0
            # while i <= down:
                # j = left
                # while j <= right:
                    # if defend.grid[i][j] == '.':
                        # counter += 1
                    # j += 1
                # i += 1
            # if counter == 0:
                # size += 1
                
           
            # else:
        
                # m = random.randint(0, counter - 1)
                # j = left
                # i = up
                # while i <= down:
                    # j = left
                    # while j <= right:
                    
                        # if defend.grid[i][j] == '.' and m == 0:
                            # return (i, j)
                        # if defend.grid[i][j] == '.' and m != 0:
                            # m -= 1
                        
                        # j += 1
                    # i += 1
                
                
        
        
    
    #You probably need quite a few other functions
    def check_win(self, state, r, c):
        n_count = self.get_continuous_count(state.grid, r, c, -1, 0)
        s_count = self.get_continuous_count(state.grid, r, c, 1, 0)
        e_count = self.get_continuous_count(state.grid, r, c, 0, 1)
        w_count = self.get_continuous_count(state.grid, r, c, 0, -1)
        se_count = self.get_continuous_count(state.grid, r, c, 1, 1)
        nw_count = self.get_continuous_count(state.grid, r, c, -1, -1)
        ne_count = self.get_continuous_count(state.grid,r, c, -1, 1)
        sw_count = self.get_continuous_count(state.grid, r, c, 1, -1)
        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or \
                (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            return True  #game over


    def get_continuous_count(self, grid, r, c, dr, dc):
        piece = grid[r][c]           #know it is 'b'or 'w'
        # print "get_continuous_count", piece
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.grid_size and 0 <= new_c < self.grid_size:
                if grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result
    
    def set_piece(self, grid, piece, r, c):
        if grid[r][c] == '.':
            grid[r][c] = piece
            if piece[0] == 'b':
                piece[0] = 'w'
            else:
                piece[0] = 'b'
            return True
        return False