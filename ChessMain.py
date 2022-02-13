#GameState File
import pygame as p
from Engine import ChessEngine
width=height=512
dimension=8
sqr_size=height//dimension
max_fps=15
images={}

def loadImages():
    pieces=['wP','wR','wN','wB','wQ','wK','bP','bB','bN','bR','bQ','bK']
    for piece in pieces:
        images[piece]=p.transform.scale(p.image.load("Engine/Pieces/"+piece+".png"),(sqr_size,sqr_size))

#Main Driver
def main():
    p.init()
    screen=p.display.set_mode((width,height))
    clock=p.time.Clock()
    screen.fill(p.Color("white"))
    gs=ChessEngine.GameState()
    loadImages()
    running=True
    while running:
        for e in p.event.get():
            if e.type== p.QUIT:
                running=False
        drawGameState(screen,gs)
        clock.tick(max_fps)
        p.display.flip()

#Responsible for graphics within the gamestate
def drawGameState(screen,gs):
    drawBoard(screen)#Squares on board
    drawPieces(screen,gs.board)#Pieces on board

def drawBoard(screen):
    colors=[p.Color("aquamarine"),p.Color("cadetblue")]
    for r in range(dimension):
        for c in range(dimension):
            color=colors[((r+c)%2)]
            p.draw.rect(screen,color,p.Rect(c*sqr_size,r*sqr_size,sqr_size,sqr_size))

def drawPieces(screen,board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece!="--":
                screen.blit(images[piece],p.Rect(c*sqr_size,r*sqr_size,sqr_size,sqr_size))

if __name__=="__main__":
    main()