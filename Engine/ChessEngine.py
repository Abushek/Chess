#CurrentState of Chess game and valid moves
class GameState():

    def __init__(self):
        #Board is a 8x8 2D List containing 2 character elements
        #First character represents whether White,Black or Blank
        #Second character represents the piece 
        self.board=[
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wP","wP","wP","wP","wP","wP","wP","wP"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]]
        self.whiteToMove=True
        self.moveLog=[]

    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove=not self.whiteToMove
        
class Move():

    ranksToRows={"1":7,"2":6,"3":5,"4":4,
                 "5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}
    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSqr,endSqr,board):
        self.startRow=startSqr[0]
        self.startCol=startSqr[1]
        self.endRow=endSqr[0]
        self.endCol=endSqr[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
        