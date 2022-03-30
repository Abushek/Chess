#GameState File
from tkinter.tix import IMAGE
import pygame as p
from Engine import ChessEngine,SmartMoveFinder
from multiprocessing import Process,Queue
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
    animate = False #Flag for animating a move
    loadImages()
    gameOver=False
    running=True
    sqselect=()#(row,col)
    playerClicks=[]#Keeps track of player clicks(two tuples: [#Initial(row6,col4),#Final(row4,row4)])
    playerOne = False #If Human plays white, then this is True, If AI is playing then its False
    playerTwo = False
    AIThinking = False
    moveFinderProcess = None
    moveUndone =False
    while running:
        humanTurn= (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type== p.QUIT:
                running=False
            #mouse handler
            elif e.type==p.MOUSEBUTTONDOWN:
                if not gameOver:
                    location=p.mouse.get_pos()
                    col=location[0]//sqr_size
                    row=location[1]//sqr_size
                    if sqselect == (row,col):
                        sqselect=()#Deselect
                        playerClicks=[]
                    else:
                        sqselect=(row,col)
                        playerClicks.append(sqselect)
                    if len(playerClicks) == 2 and humanTurn:
                        move=ChessEngine.Move(playerClicks[0],playerClicks[1],gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade=True
                                animate=True
                                sqselect=()
                                playerClicks=[]
                        if not moveMade:
                            playerClicks=[sqselect]
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade=True
                    animate=False
                    gameOver = False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking=False
                    moveUndone=True
                if e.key == p.K_r:
                    gs=ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqselect=()
                    playerClicks=[]
                    moveMade=False
                    animate=False
                    gameOver=False
                    if AIThinking:
                        moveFinderProcess.terminate()
                        AIThinking=False
                    moveUndone=True

        #AI Move Finder
        if not gameOver and not humanTurn and not moveUndone:
            if not AIThinking:
                AIThinking=True
                print("Thinking...")
                returnQueue =Queue()
                moveFinderProcess=Process(target=SmartMoveFinder.findBestMoveNew,args=(gs,validMoves,returnQueue))
                moveFinderProcess.start()

            if not moveFinderProcess.is_alive():
                print("Done Thinking")
                AIMove = returnQueue.get()
                if AIMove is None:
                    AIMove = SmartMoveFinder.findRandomMove(validMoves)
                gs.makeMove(AIMove)
                moveMade = True
                animate = True
                AIThinking=False
            
        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1],screen,gs.board,clock)
            validMoves=gs.getValidMoves()
            moveMade=False
            animate=False
            moveUndone =False
        drawGameState(screen,gs,validMoves,sqselect)
        if gs.checkMate:
            gameOver=True
            if gs.whiteToMove:
                drawText(screen,"Black wins by Checkmate")
            else:
                drawText(screen,"White wins by Checkmate")
        elif gs.staleMate:
            gameOver=True
            drawText(screen,'Stalemate')
        
        clock.tick(max_fps)
        p.display.flip()

#Highlight Square selected and moves for pieces 
def highlightSquares(screen,gs,validMoves,sqSelected):
    if sqSelected!=():
        r,c=sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'):
            #Highlight selected square
            s=p.Surface((sqr_size,sqr_size))
            s.set_alpha(100)
            s.fill(p.Color('blue'))
            screen.blit(s,(c*sqr_size,r*sqr_size))
            #Highlight moves
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s,(move.endCol*sqr_size,move.endRow*sqr_size))
#Responsible for graphics within the gamestate
def drawGameState(screen,gs,validMoves,sqSelected):
    drawBoard(screen)#Squares on board
    highlightSquares(screen,gs,validMoves,sqSelected)
    drawPieces(screen,gs.board)#Pieces on board

def drawBoard(screen):
    global colors
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

def animateMove(move,screen,board,clock):
    global colors 
    dR=move.endRow-move.startRow
    dC=move.endCol-move.startCol
    framesPerSquare=5
    frameCount=(abs(dR)+abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r,c=(move.startRow+dR*frame/frameCount,move.startCol+dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen,board)
        #erase the piece moved from its ending square
        color=colors[(move.endRow+move.endCol)%2]
        endSquare=p.Rect(move.endCol*sqr_size,move.endRow*sqr_size,sqr_size,sqr_size)
        p.draw.rect(screen,color,endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured!='--':
            if move.isEnpassantMove:
                enPassantRow=(move.endRow+1) if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*sqr_size,enPassantRow*sqr_size,sqr_size,sqr_size)
            screen.blit(images[move.pieceCaptured],endSquare)
        #draw moving piece
        screen.blit(images[move.pieceMoved],p.Rect(c*sqr_size,r*sqr_size,sqr_size,sqr_size))
        p.display.flip()
        clock.tick(60)
def drawText(screen,text):
    font=p.font.SysFont("Helvitca",32,True,False)
    textObject = font.render(text,0,p.Color('Gray'))
    textLocation=p.Rect(0,0,width,height).move(width/2-textObject.get_width()//2,height/2-textObject.get_height()//2)
    screen.blit(textObject,textLocation)
    textObject = font.render(text,0,p.Color('Black'))
    screen.blit(textObject,textLocation.move(2,2))
if __name__=="__main__":
    main()