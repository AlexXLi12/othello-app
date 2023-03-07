import pygame, sys
import othello.constants as const
from othello.classes import *
from othello.rules import *
import othello.engine as engine
from tkinter import messagebox
# initialization
WINDOW = pygame.display.set_mode((const.WIDTH,const.HEIGHT))
pygame.display.set_caption('Othello')

#initialize 8x8 board with 64 Square sprites
board = []
for k in range(0, const.HEIGHT, const.HEIGHT//8):
    for i in range(0, const.WIDTH, const.WIDTH//8):
        square = Square((i, k), const.WIDTH//8)
        #starting position
        if k//(const.HEIGHT//8) == 3:
            if i//(const.WIDTH//8) == 3:
                square.placePiece(1)
            elif i//(const.WIDTH//8) == 4:
                square.placePiece(-1)
        if k//(const.HEIGHT//8) == 4:
            if i//(const.WIDTH//8) == 3:
                square.placePiece(-1)
            if i//(const.WIDTH//8) == 4:
                square.placePiece(1)
        WINDOW.blit(square.image, square.rect)
        board.append(square)

#if playerTurn =-1, color = colorwheel[-1] = const.BLACK;
#if playerTurn = 1, color = colorwheel[1] = const.WHITE;
colorwheel = [0,const.WHITE, const.BLACK]

def resetPossibles(window, board):
    """Reset all possible move squares back to green

    Args:
        board (list): list of Square objects representing the Othello board
        window (pygame.Surface): window of the game
    """
    for square in board:
        if square.color == const.YELLOW:
            square.setColor(GREEN)
            window.blit(square.image, square.rect)
# main function
def main():
    global board
    clock = pygame.time.Clock()
    run = True
    mouseDown = False
    playerTurn = -1
    possibles = possibleMoves(board, playerTurn)
    while run:
        mouseDown = False
        clock.tick(30)
        #process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown = True
        #engine move
        if len(possibles) == 0:
            engine_idx = engine.calcMove(board, playerTurn*-1)
            if engine_idx == -1: #no possible moves
                run = False
                break
            else:
                board = updateBoard(board, playerTurn*-1, engine_idx)
                possibles = possibleMoves(board, playerTurn)
        for idx in possibles:
            square = board[idx]
            square.setColor(const.YELLOW)
            #if mouse is hovered over square
            if square.rect.collidepoint(pygame.mouse.get_pos()):
                #if mouse is hovered over square AND mouseDown, place a piece
                if mouseDown:
                    resetPossibles(WINDOW,board) #reset previously marked "possible" squares
                    board = updateBoard(board,playerTurn,idx)
                    #update to show player has moved before engine move
                    for sq in board:
                        WINDOW.blit(sq.image, sq.rect)
                        pygame.display.update()
                    #engine move
                    engine_idx = engine.calcMove(board, playerTurn*-1)
                    board = updateBoard(board, playerTurn*-1, engine_idx)
                    possibles = possibleMoves(board, playerTurn)
                    break
            #update square onto window
        for square in board:
            WINDOW.blit(square.image, square.rect)
        pygame.display.update()
    

if __name__ == '__main__':
    main()