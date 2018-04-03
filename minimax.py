

from math import sqrt, log,e
import random
import copy
from randplay import *



class State:
    def __init__(self, grid, player, r, c):
        self.grid = grid;
        self.pos = (r, c);
        self.player = player;
        self.children = [];    #element is the index of the tree node list's index
        self.index = -1;
        self.parent = -1;
        self.score = -1000000;
        
        
class MinimaxTree:
    #nextPlayer: next step player color
    #r, c : previous step pos
    #grid: current board
    def __init__(self, grid, nextPlayer, r, c):
        # print 'next color is ', nextPlayer;
        self.grid = grid;
        self.nextPlayer = nextPlayer;
        self.preRow = r;
        self.preCol = c;
        self.gridSize = len(grid);            #grid size
        
        # for i in range (self.gridSize):
            # for j in range (self.gridSize):
                # if grid[i][j] == 'w' or grid[i][j] == 'b':
                    # print i,':', j;
                    
        # print '~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~``';
        
        
        #if it was the first step, root is a imagine pos
        #if it was not first step, root is previous step on the board
        self.rootPlayer = 'w' if self.nextPlayer == 'b' else 'b';
        if r == -1 and c == -1:
            self.preRow = self.gridSize / 2;
            self.preCol = self.gridSize / 2;
            

        
            
        self.root = State(self.grid, self.rootPlayer, self.preRow, self.preCol);     #set root
        
        self.gridNode = [];                  #all node in the tree,element type:State
        self.gridNodeIndex = 0;
        self.gridNode.append(self.root);     #insert root into treenodes list
        self.gridNodeIndex += 1;
        self.root.index = 0;
        self.layers = 4              #minimaxtree is 4 layers
        self.build_tree (1, self.rootPlayer, self.root);   #call tree build func
        # print ("finished build tree ");
        # test child of root
        # for i in self.root.children:
            # print self.gridNode[i].pos;
        #for alpha beta tree pruning
        self.alpha = -1000000;
        self.beta = 1000000;
        
        self.find_score;
        
        
    def find_score(self):
        
        
        
        
        firstValue = -1000000;
        firstIndex = -1;
        #find the root's children's score by alpha_beta
        for c in self.root.children:   #c is index of gridNode
            # raw_input("child: ")
            # print self.gridNode[c].pos
            # print "child's color", self.gridNode[c].player
            
            
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~need make change
            
            score = self.find_reward(self.gridNode[c].pos[0], self.gridNode[c].pos[1], self.gridNode[c].player, self.gridNode[c].grid);
            if score >= 10000:
                if firstValue < score:
                   firstValue = score 
                   firstIndex = c
                     
            self.gridNode[c].score = self.alpha_beta(self.gridNode[c], self.alpha, self.beta, 1);
            
        if firstValue != -1000000:
            self.gridNode[firstIndex].score = 1000000;
        
        
   
    def next_step (self):
        r, c = (-1, -1);
        value = -1000000;
        # print 'size of children is ', len(self.root.children);
        for i in self.root.children:
                if self.gridNode[i].score >= value:
                    value = self.gridNode[i].score;
                    r, c = self.gridNode[i].pos;
                    
        return r, c;
                
        
    #setting a range for possible chess pos, at least 3 grid there is a 'b' or 'w'
    def check_range (self, r, c, board):
        # print "func check_range", r, ' ', c
        up = r;
        down = r;
        left = c;
        right = c;
        while up - 1 >= 0 and up >= r - 0 :
            up -= 1;
        while down + 1 < self.gridSize and down <= r + 0:
            down += 1;
        while left - 1 >= 0 and left >= c - 0:
            left -= 1;
        while right + 1 < self.gridSize and right <= c + 0:
            right += 1;
         
        
        # print ("up is ", up, ' down is ', down, ' left is ', left, ' right is ', right);
        for i in range(up, down + 1):
            for j in range(left, right + 1):
                if board[i][j] == 'b' or board[i][j] == 'w':
                    return True;
        return False;
        
        
    def build_tree (self, layers, whoPlay, parent):
        if layers != self.layers:
            
            layers += 1;
            # print 'the root is ',parent.pos
            
            self.build_one_layer(parent);
            
            # for i in range (self.gridSize):
                # for j in range (self.gridSize):
                    # if parent.grid[i][j] == 'w' or parent.grid[i][j] == 'b':
                        # print i,':', j;
            # raw_input('root pause');

            whoPlay = 'b' if whoPlay == 'w' else 'w'
            for c in range(len(parent.children)):
                self.build_tree(layers, whoPlay, self.gridNode[parent.children[c]]);
    
    #pos is on the board
    def is_valid (self, r, c):
        if r >= 0  and r < self.gridSize and c >= 0 and c < self.gridSize:
            return True;
        return False;
                
   
        
    #iterator from center by helix direction   
    def build_one_layer(self, parent):
        # print ("parent's index is ", parent.index, parent.pos, parent.player);
        r_center = parent.pos[0];
        c_center = parent.pos[1];
        move = 1;     #helix move distance
        cursor = [];
        cursor.append(r_center)
        cursor.append(c_center);
        optPlayer = 'w' if parent.player == 'b' else 'b';
        
        while True:
            #up
            cursor[0] = cursor[0] - 1;
            
            #right
            #need check range           
            c = 0;
            # print 'right', move;
            while c < move: 
                c += 1;
                cursor[1] = cursor[1] + 1
                if self.is_valid(cursor[0], cursor[1]) :
                    self.new_node(parent, optPlayer, cursor[0], cursor[1]);
                   
                
           #down
            r = 0;
            # print 'down', move*2
            while r < move * 2 :
                r += 1;
                cursor[0] = cursor[0] + 1;
                if self.is_valid(cursor[0], cursor[1]):
                    self.new_node(parent, optPlayer, cursor[0], cursor[1]);
                    
                    
            #left
            c = 0;
            # print 'left', move * 2
            while c < move * 2 :
                c += 1;
                cursor[1] = cursor[1] - 1;
                
                if self.is_valid(cursor[0], cursor[1]):
                    # print 'func', cursor[0], cursor[1];
                    self.new_node(parent, optPlayer, cursor[0], cursor[1]);
                    
                
            #up
            r = 0;
            # print 'up', move*2
            while r < move * 2 :
                r += 1;
                cursor[0] = cursor[0] - 1;
                if self.is_valid(cursor[0], cursor[1]):
                    self.new_node(parent, optPlayer, cursor[0], cursor[1]);
                
            #right
            c = 0;
            # print 'right', move
            while c < move : 
                c += 1;
                cursor[1] = cursor[1] + 1;
                if self.is_valid(cursor[0], cursor[1]):
                    self.new_node(parent, optPlayer, cursor[0], cursor[1] );
                    
                  
                    
                
            move += 1;
            if move >= self.gridSize:
                break;
                
            
        
    
    
    def new_node(self, parent, whoPlay, r, c):
        
        # print parent.grid[0][0];
        # print r, c;
        if self.check_range(r, c, parent.grid) and parent.grid[r][c] == '.':
            # print "func new_node", r, c;
            childNode = State(copy.deepcopy(parent.grid), whoPlay, r, c);
            childNode.grid[r][c] = whoPlay;
                        
                        # update tree nodes list, nodelist's index
                        # child state's index, parent, 
                        # parent state's children list 
            self.gridNode.append(childNode);
            childNode.index = self.gridNodeIndex;
            childNode.parent = parent.index;
            parent.children.append(childNode.index);
            self.gridNodeIndex += 1;
                    
    #alpha_beta pruning algorithm                
    def alpha_beta (self, node, a, b, layers): 
        #leaf node is rival play, so we get negative value of the reward 
        if len(node.children) == 0:
            node.score = self.find_reward(node.pos[0], node.pos[1], node.player, node.grid);
            # print "leaf ", node.pos
            # print " leaf value is ", node.score;
            return node.score;
        
        if node.player != self.nextPlayer:
            # print "max: " , node.pos
            value = -1000000;
            # current = self.find_reward(node.pos[0], node.pos[1], node.player, node.grid);
            # if current >
            for c in node.children:
                value = max(value, self.alpha_beta(self.gridNode[c], a, b, 1))
                
                #node is root, such that node children are the possible first step
                    #need to do =
                    
                
                
                a = max(a, value);
                if a >= b:
                    break;
            # print "!!!!!!!!!!!!!!!1"        
            # print "max value is ", value;
            return value;
        if node.player == self.nextPlayer:
            # print "min: ", node.pos
            # print "_____________________________"
            value = 1000000;
            

            
            for c in node.children:
                value = min(value, self.alpha_beta(self.gridNode[c], a, b, 1));
               
                b = min(b, value);
                if a >= b:
                    break;
            # print "???????????????????????????/"
            # print "min value is ", value;
            return value ;
            
    
    
    
    def find_reward (self, row, col, player, board):
        #  key is line's string, value[0] -length, value[1] - 2 = active, 1=sleep, 0 = dead
        format = {};
        format['w_e'] = [];
        format['n_s'] = [];
        format['ws_en'] = [];
        format['wn_es'] = [];
        
        self.check_length(board, row, col, format);
        optPlayer = 'b' if player == 'w' else 'w';
              
        #long five
        for i in format:
            if format[i][0] >= 5:
                return 100000
        
        
        #defend four.
        if self.chess_on_line(row, col, optPlayer, board, 4):
            return 50000
        
        
        #active four
        for i in format:
            if format[i][0] == 4 and format[i][1] == 2:
                return 20000;
       
        #two sleep four
        counter = 0;
        for i in format:
            if format[i][0] == 4 and format[i][1] == 1:
                counter += 1;
        if counter >= 2:        
            return 20000;
            
        
        #sleep four and active 3
        counter_four = 0;
        counter_three = 0;
        for i in format:
            if format[i][0] == 4 and format[i][1] == 1:   #sleep four
                counter_four += 1;
            if format[i][0] == 3 and format[i][1] == 2:   #active three
                counter_three += 1;
                
        if counter_four >= 1 and counter_three >= 1:
            return 20000
            
            
        #defend three  
        if self.chess_on_line(row, col, optPlayer, board, 3):
            return 10000;
            
        #two active 3
        counter = 0;
        for i in format:
            if format[i][0] == 3 and format[i][1] == 2:
                counter += 1;
        if counter >= 2:
            return 5000;
            
        #one active 3, and one sleep 3
        counter_a_three = 0;
        counter_s_three = 0;
        for i in format:
            if format[i][0] == 3 and format[i][1] == 2:
                counter_a_three += 1;
            if format[i][0] == 3 and format[i][1] == 1:
                counter_s_three += 1;
        if counter_a_three == 1 and counter_s_three == 1:
            return 1000;
            
        #sleep 4
        for i in format:
            if format[i][0] == 4 and format[i][1] == 1:
                return 500;
        
        
        #active 3
        for i in format:
            if format[i][0] == 3 and format[i][1] == 2:
                return 200;
        
        #two active 2:
        counter_two = 0;
        for i in format:
            if format[i][0] == 2 and format[i][1] == 2:
                counter_two += 1;
        if counter_two >= 2:
            return 100;
            
            
        #sleep 3:
        for i in format:
            if format[i][0] == 3 and format[i][1] == 1:
                return 50;
        
        #active 2 and sleep 2:
        counter_a_two = 0;
        counter_s_two = 0;
        for i in format:
            if format[i][0] == 2 and format[i][1] == 2:
                counter_a_two += 1;
            if format[i][0] == 2 and format[i][1] == 1:
                counter_s_two += 1;
        
        if counter_a_two >= 1 and counter_s_two >= 1:
            return 10;
            
            
        #active 2
        counter = 0;
        for i in format:
            if format[i][0] == 2 and format[i][1] == 2:
                return 5;
          
        #sleep 2
        for i in format:
            if format[i][0] == 2 and format[i][1] == 1:
                return 3;
                
        #active 1
        for i in format:
            if format[i][0] == 1 and format[i][1] == 2:
                return 1;
                
        #dead 4/3/2/1
        for i in format:
            if (format[i][0] == 4 or format[i][0] == 3 or format[i][0] == 2 or format[i][0] == 1) and format[i][1] == 0:
                return -5;
        
        return 0;
        
      
        
     #check one chess block a active four or three
     #there are 8 different direction
    def chess_on_line(self, row, col, player, board, length):
        #up
        valueTest = True;
        if row - length >= 0:
            
            for i in range(1, length + 1):
                if board[row - i][col] != player:
                    valueTest = False;
                    break;
        else:
            valueTest = False;
        if valueTest:
            # print 'func chess_on_line,  up';
            return valueTest;
        
        #down
        valueTest = True;
        if row + length < self.gridSize:
            for i in range(1, length + 1):
                if board[row + i][col] != player:
                    valueTest = False;
                    break;
        else:
            valueTest = False;
        if valueTest:
            return valueTest;
            
        #east
        valueTest = True;
        if col + length < self.gridSize:
            for i in range(1, length + 1):
                if board[row][col + i] != player:
                    valueTest = False;
                    break;
        else:
            valueTest = False;
        if valueTest:
            return valueTest;
            
        #west
        valueTest = True;
        if col - length >= 0:
            for i in range(1, length + 1):
                if board[row][col - i] != player:
                    valueTest = False;
                    break;
        else:
            valueTest = False;
        if valueTest:
            return valueTest;
        
        #w_n
        valueTest = True;
        if col - length >= 0 and row - length >= 0:
            for i in range(1, length + 1):
                if board[row - i][col - i] != player:
                    valueTest = False;
                    break;
        else:
            valueTest = False;
        if valueTest:
            return valueTest;
            
        #w_s
        valueTest = True;
        if col - length >= 0 and row + length < self.gridSize:
            for i in range(1, length + 1):
                if board[row + i][col - i] != player:
                    valueTest = False;
                    break;
        else:
            valueTest = False;
        if valueTest:
            return valueTest;
            
            
        #e_n
        valueTest = True;
        if col + length < self.gridSize and row - length >= 0:
            for i in range(1, length + 1):
                if board[row - i][col + i] != player:
                    valueTest = False;
                    break;
        else:
            valueTest = False;
        if valueTest:
            return valueTest;
            
        #e_s
        valueTest = True;
        if col + length < self.gridSize and row + length < self.gridSize:
            for i in range(1, length + 1):
                if board[row + i][col + i] != player:
                    valueTest = False;
                    break;
                    
        else:
            valueTest = False;
        if valueTest:
            return valueTest;
            
        
        
                    
        
     
    
    #param: chess board / chess place(r,c) / format list
    #output: 5 on same line and save 8 direction information(length, active/dead);
    def check_length(self, board, r, c, format):
        n_count = self.get_continuous_count(board, r, c, -1, 0)
        s_count = self.get_continuous_count(board, r, c, 1, 0)
        e_count = self.get_continuous_count(board, r, c, 0, 1)
        w_count = self.get_continuous_count(board, r, c, 0, -1)
        se_count = self.get_continuous_count(board, r, c, 1, 1)
        nw_count = self.get_continuous_count(board, r, c, -1, -1)
        ne_count = self.get_continuous_count(board,r, c, -1, 1)
        sw_count = self.get_continuous_count(board, r, c, 1, -1)
        
        win = False;
        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or \
                (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            win = True;  #game over
        
        format['w_e'].append(e_count + w_count + 1);
        format['n_s'].append(n_count + s_count + 1 );
        format['ws_en'].append(ne_count + sw_count + 1);
        format['wn_es'].append(se_count + nw_count + 1 );
        
        
        #update format information for easy find the reward
        #north south
        number = 0;    #calculate active, sleep, dead
        if r - n_count -1 >= 0 and board[r - n_count - 1][c] == '.':
            number += 1;
        if r + s_count + 1 < self.gridSize and board[r + s_count + 1][c] == '.':
            number += 1;
        format['n_s'].append(number);
            
        #east west
        number = 0;
        if c - w_count -1 >= 0 and board[r][c - w_count - 1] == '.':
            number += 1;
        if c + e_count + 1 < self.gridSize and board[r][c + e_count + 1] == '.':
            number += 1;
        format['w_e'].append(number);
        
        #s_e to n_w
        number = 0;
        if r + se_count + 1 < self.gridSize and c + se_count + 1 < self.gridSize and board[r + se_count + 1][c + se_count + 1] == '.':
            number += 1;
        if r - nw_count -1 >= 0  and c -nw_count -1 >=0 and board[r - nw_count -1][c - nw_count -1]== '.':
            number += 1;
        format['wn_es'].append(number);
        
        #n_e to s_w
        number = 0;
        if r + sw_count + 1 < self.gridSize and c -sw_count -1 >= 0  and board[r + sw_count + 1][c - sw_count -1] == '.':
            number += 1;
        if r - ne_count -1 >= 0 and c + ne_count + 1 < self.gridSize and board[r - ne_count -1][c + ne_count + 1] == '.':
            number += 1;
        format['ws_en'].append(number);
        
        
        
        return win;
            
    def get_continuous_count(self, grid, r, c, dr, dc):
        piece = grid[r][c]           #know it is 'b'or 'w'
        # print "get_continuous_count", piece
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.gridSize and 0 <= new_c < self.gridSize:
                if grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result
        
        