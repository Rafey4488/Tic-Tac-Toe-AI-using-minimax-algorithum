import sys
import copy
import pygame
import numpy as np
import random
from const import *


pygame.init()
sc = pygame.display.set_mode((Width, Height))
pygame.display.set_caption("TIC TAC TOE BY: M.RAFEY")

sc.fill(B_Color)

class Board:
    def __init__ (self):
        self.squares = np.zeros( (Rows, Columns) )
        self.emp_sqrs = self.squares 
        self.marked_sqrs = 0

    def final_st(self, show = False):
        #final state will return 0 if there id draw. 1 if player 1 wins and 2 if player 2 wins.

        #for vartical winns
        for col in range(Columns):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    Line_color = circle_color if self.squares[0][col] == 2 else dec_cross_color 
                    initial_pos = (col * Boxsize + Boxsize //2, 20)
                    final_pos = (col * Boxsize + Boxsize //2, Height - 20)
                    pygame.draw.line(sc, Line_color, initial_pos, final_pos, Line_Width)
                return self.squares[0][col]
        #horizontal
        for row in range(Rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    Line_color = circle_color if self.squares[row][0] == 2 else dec_cross_color
                    initial_pos = (20, row * Boxsize + Boxsize //2)
                    final_pos = (Width - 20, row * Boxsize + Boxsize //2)
                    pygame.draw.line(sc, Line_color, initial_pos, final_pos, Line_Width)
                return self.squares[row][0]
        #Diagnol
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2]!= 0:
            if show:
                Line_color = circle_color if self.squares[1][1] == 2 else dec_cross_color
                initial_pos = (20, 20)
                final_pos = (Width - 20, Height - 20)
                pygame.draw.line(sc, Line_color, initial_pos, final_pos, cross_width)
            return self.squares[1][1]
        #decending diognal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2]!= 0:
            if show:
                Line_color = circle_color if self.squares[1][1] == 2 else dec_cross_color
                initial_pos = (20, Height - 20)
                final_pos = (Width - 20, 20)
                pygame.draw.line(sc, Line_color, initial_pos, final_pos, cross_width)
            return self.squares[1][1]
        #none
        return 0
        

    def M_sqr(self, row, col, P1):
        self.squares[row][col] = P1
        self.marked_sqrs += 1

    #empty square
    def emp_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqr(self):
        emp_sqrs = []
        for row in range(Rows):
            for col in range(Columns):
                if self.emp_sqr(row,col):
                    emp_sqrs.append((row,col))

        return emp_sqrs 
                
    #check when board is full
    def IsFull(self):
        return self.marked_sqrs == 9

    def Isempty(self):
        return self.marked_sqrs == 0 
#1 X
#2 O

#AI CLASS
class ai:
    def __init__(self, level=1, P1=2):
        self.level = level
        self.P1 = P1
    
     #random empty square on the board    
    def rnd(self, board):
        emp_sqrs = board.get_empty_sqr()
        i = random.randrange(0, len(emp_sqrs))
        return emp_sqrs[i] # row col

    def minimax(self, board, maximize):

        case = board.final_st() #has 0 1 or 2
        #Player 1 wining
        if case == 1:
            return 1, None # eval , move
        #AI is player 2 return -1 bcz we are minimizing
        if case == 2:
            return -1, None
        # draw check
        if board.IsFull():
            return 0, None
        
        if maximize:
            max_evaluation = -100 # any number greater tham 0 1 -1
            best_move = None
            emp_sqrs = board.get_empty_sqr()

            for (row, col) in emp_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.M_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]#false because next move is minimizing player [0] to access the position
                # It will return 2 things evaluation 1 2 or 0 and best move as tuple
                if eval > max_evaluation: 
                    max_evaluation = eval
                    best_move = (row, col)
            
            return max_evaluation, best_move

        elif not maximize:
            min_evaluation = 100 # any number greater tham 0 1 -1
            best_move = None
            emp_sqrs = board.get_empty_sqr()

            for (row, col) in emp_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.M_sqr(row, col, self.P1)
                eval = self.minimax(temp_board, True)[0]#Recursion and true for change player [0] to access the position
                # It will return 2 things evaluation 1 2 or 0 and best move as tuple
                if eval < min_evaluation: 
                    min_evaluation = eval
                    best_move = (row, col)
            
            return min_evaluation, best_move

    def eval(self, main_board):
        if self.level == 0:
             eval = 'random'
             move = self.rnd(main_board)# false for minimizing
     
        else:
            eval, move = self.minimax(main_board, False)
        
        print(f"AI marked in position: {move} with evaluation of {eval}")
        return move


class Game:
    def __init__(self):
        self.board = Board()
        self.AI = ai()
        self.P1 = 1
        self.gameMode = 'AI'#ai aur player vs player
        self.running = True
        self.V_H_line()

    def make_move(self, row, col):
        self.board.M_sqr(row, col, self.P1)
        self.draw(row,col)
        self.change_player()



    def V_H_line(self):

        sc.fill( B_Color )
        #vartical
        pygame.draw.line(sc, Line_color, (Boxsize, 0), (Boxsize, Height), Line_Width)
        pygame.draw.line(sc, Line_color, (Width - Boxsize, 0), (Width - Boxsize, Height), Line_Width)

        #horizontal axis
        pygame.draw.line(sc, Line_color, (0, Boxsize), (Width, Boxsize), Line_Width)
        pygame.draw.line(sc, Line_color, (0, Height - Boxsize), (Width, Height - Boxsize), Line_Width)


    #connecting console with gui and sending all info from console to gui
    #creating circle and cross


    def draw(self, row, col):
        if self.P1 == 1:
            #cross
            #Assending Line
                         # X axis                  Y axis 
            start_Ase = (col * Boxsize + offset, row * Boxsize + Boxsize - offset)
            end_Ase = (col * Boxsize + Boxsize - offset, row * Boxsize + offset)
            pygame.draw.line(sc, dec_cross_color, start_Ase, end_Ase, cross_width)
            #Dessending line
            start_dec = (col * Boxsize + offset, row * Boxsize + offset)
            end_dec = (col * Boxsize + Boxsize - offset, row * Boxsize + Boxsize - offset)
            pygame.draw.line(sc, dec_cross_color, start_dec, end_dec, cross_width)
        elif self.P1 == 2:
            #circle
            center = (col * Boxsize + Boxsize // 2, row * Boxsize + Boxsize // 2)
            pygame.draw.circle(sc, circle_color, center, rad, circle_width)

    #next player e.g if player = 1 then 1%2 will be 1 & 1+1 = 2 turn. if 2 2%2 = 0 + 1 = 1 turn
    def change_player(self):
        self.P1 = self.P1 % 2 + 1

    def change_mode(self):
        self.gameMode = 'AI' if self.gameMode == 'pvp' else 'pvp'

    def over(self):
        return self.board.final_st(show = True) != 0 or self.board.IsFull()
        
    def reset(self):
        self.__init__()

def main():
    #game object
    game = Game()
    board = game.board
    AI = game.AI


    #MAINLOOP
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


                #key eventss
            if event.type == pygame.KEYDOWN:
                # c  to change gamemode
                if event.key == pygame.K_c:
                    game.change_mode()
                    print('Game Mode Changed')
                    
                    
                
                #reset r
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    AI = game.AI
                    print('Board Reset')
                    print('Unbeatable Ai Mode')


                # 1 to random ai 
                if event.key == pygame.K_1:
                    AI.level = 0
                    print('Random Ai mode')

                # 2 to random ai 
                if event.key == pygame.K_2:
                    AI.level = 1
                    print('Unbeatable Ai Mode')

    #here i am describing an event which sends all info from gui to console and also not using pixel values in array
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // Boxsize
                col = pos[0] // Boxsize

                if board.emp_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.over():
                        game.running = False
                        print('Game Over')
                       
                
        if game.gameMode == 'AI' and game.P1 == AI.P1 and game.running:

            pygame.display.update()
            #ai func
            row, col = AI.eval(board)
            game.make_move(row, col)
            
            if game.over():
                game.running = False
                print('Game Over')
                
             

        pygame.display.update()

main()
