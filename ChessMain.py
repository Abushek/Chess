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
    validMoves=gs.getValidMoves()
    moveMade= False #Flag for move

    loadImages()
    running=True
    sqselect=()#(row,col)
    playerClicks=[]#Keeps track of player clicks(two tuples: [#Initial(row6,col4),#Final(row4,row4)])

    while running:
        for e in p.event.get():
            if e.type== p.QUIT:
                running=False
            #mouse handler
            elif e.type==p.MOUSEBUTTONDOWN:
                location=p.mouse.get_pos()
                col=location[0]//sqr_size
                row=location[1]//sqr_size
                if sqselect == (row,col):
                    sqselect=()#Deselect
                    playerClicks=[]
                else:
                    sqselect=(row,col)
                    playerClicks.append(sqselect)
                if len(playerClicks) == 2:
                    move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(validMoves[i])
                            moveMade=True
                            sqselect=()
                            playerClicks=[]
                    if not moveMade:
                        playerClicks=[sqselect]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade=True
        if moveMade:
            validMoves=gs.getValidMoves()
            moveMade=False
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