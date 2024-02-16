import copy
import random
import sys
import pygame
from constants import *
import numpy as np


#pygame setup
pygame.init()

screen=pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption('TIC TAC TOE')

screen.fill(BG_COLOR)

class Board:

    def __init__(self):
        self.squares=np.zeros((ROWS,COLS))
        self.empty_sqrs=self.squares
        self.marked_sqrs=0

    def final_state(self):

        #vertical wins
        for col in range(COLS):
            if self.squares[0][col]==self.squares[1][col]==self.squares[2][col]!=0:
                return self.squares[0][col]
            
        #horizontal wins
        for row in range(ROWS):
            if self.squares[row][0]==self.squares[row][1]==self.squares[row][2]!=0:
                return self.squares[row][0]
            
        #diagonal
            
        if self.squares[0][0]==self.squares[1][1]==self.squares[2][2]!=0:
            return self.squares[1][1]
        

        if self.squares[2][0]==self.squares[1][1]==self.squares[0][2]!=0:
            return self.squares[1][1]
            

        return 0          

    def mark_sqr(self,row,col,player):
        self.squares[row][col]=player
        self.marked_sqrs+=1

    def empty_sqr(self,row,col):
        return self.squares[row][col]==0
    
    def get_empty_sqrs(self):
        empty_sqrs=[]
        for row in  range(ROWS):
            for col in range(COLS):
                if(self.empty_sqr(row,col)):
                    empty_sqrs.append((row,col))

        return empty_sqrs

    def isFull(self):
        return self.marked_sqrs==9
    
    def isEmpty(self):
        return self.marked_sqrs==0

class AI:

    def __init__(self,level=1,player=2):
        self.level=level
        self.player=player

    def rnd(self,board):
        empty_sqrs=board.get_empty_sqrs()
        idx=random.randrange(0,len(empty_sqrs))

        return empty_sqrs[idx]

    def minimax(self,board,maximizing):
        #terminal case
        case=board.final_state()

        #player 1 wins
        if case==1:
            return 1,None

        if case==2:
            return -1,None
        
        elif board.isFull():
            return 0,None

        if maximizing:
            max_eval=-100
            best_move=None

            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,1)
                eval=self.minimax(temp_board,False)[0]
                if eval>max_eval:
                    max_eval=eval
                    best_move=(row,col)
                
            return max_eval,best_move


        elif not maximizing:
            min_eval=100
            best_move=None

            empty_sqrs=board.get_empty_sqrs()

            for (row,col) in empty_sqrs:
                temp_board=copy.deepcopy(board)
                temp_board.mark_sqr(row,col,self.player)
                eval=self.minimax(temp_board,True)[0]
                if eval<min_eval:
                    min_eval=eval
                    best_move=(row,col)
                
            return min_eval,best_move

            


    def eval(self,main_board):
        if self.level==0:
            #random choice
           
           move=self.rnd(main_board)


        else:
            #minmax algo choise
            eval,move=self.minimax(main_board,False)

        print(f'AI has chosen {move} with an  eval of :{eval}')
        return move

class Game:

    def __init__(self):
        self.show_lines()
        self.ai=AI()
        self.board=Board()
        self.player=1
        self.running=True
        self.gamemode='ai'

    def show_lines(self):
        #verticals
        pygame.draw.line(screen,LINE_COLOR,(SQSIZE,0),(SQSIZE,HEIGHT),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(WIDTH-SQSIZE,0),(WIDTH-SQSIZE,HEIGHT),LINE_WIDTH)

        #horizontals
        pygame.draw.line(screen,LINE_COLOR,(0,SQSIZE),(WIDTH,SQSIZE),LINE_WIDTH)
        pygame.draw.line(screen,LINE_COLOR,(0,HEIGHT-SQSIZE),(WIDTH,HEIGHT-SQSIZE),LINE_WIDTH)

    def next_turn(self):
        self.player=self.player%2+1

    def draw_fig(self,row,col):
        if self.player==1:

            #desc line
            start_des=(col*SQSIZE+OFFSET,row*SQSIZE+OFFSET)
            end_des=(col*SQSIZE+SQSIZE-OFFSET,row*SQSIZE+SQSIZE-OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_des,end_des,CROSS_WIDTH)

            #asec line
            start_asec=(col*SQSIZE+OFFSET,row*SQSIZE-OFFSET)
            end_asec=(col*SQSIZE+SQSIZE-OFFSET,row*SQSIZE+SQSIZE+OFFSET)
            pygame.draw.line(screen,CROSS_COLOR,start_des,end_des,CROSS_WIDTH)

        elif self.player==2:
            center=(col*SQSIZE+SQSIZE//2,row*SQSIZE+SQSIZE//2)
            pygame.draw.circle(screen,CIRC_COLOR,center,RADIUS,CIRC_WIDTH)
        

def main():

    #object

    game=Game()
    board=game.board
    ai=game.ai

    while True:

        for event in pygame.event.get():

            if(event.type==pygame.QUIT):
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN:
                pos=event.pos
                row=pos[1]//SQSIZE
                col=pos[0]//SQSIZE

                if board.empty_sqr(row,col):
                    board.mark_sqr(row,col,game.player)
                    game.draw_fig(row,col)
                    game.next_turn()

        if game.gamemode=='ai' and game.player == ai.player:
            pygame.display.update()

            row,col=ai.eval(board)
            board.mark_sqr(row,col,game.player)
            game.draw_fig(row,col)
            game.next_turn()
        
        pygame.display.update()
main()