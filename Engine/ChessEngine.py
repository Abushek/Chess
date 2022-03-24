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
        self.moveFunctions={'P':self.getPawnMoves,'R':self.getRookMoves,'N':self.getKnightMoves,
                            'B':self.getBishopMoves,'Q':self.getQueenMoves,'K':self.getKingMoves}
        self.whiteToMove=True
        self.moveLog=[]
        self.whiteKingLocation=(7,4)
        self.blackKingLocation=(0,4)
        self.inCheck = False
        self.pins=[]
        self.checks=[]
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible=()#Coordinates for the en passant square
        self.currentCastlingRight=CastleRights(True,True,True,True)
        self.castleRightsLog=[CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                           self.currentCastlingRight.wqs,self.currentCastlingRight.bqs)]
        

    #This is not going to work for castle,pawn promotion and en-passant
    def makeMove(self,move):
        self.board[move.startRow][move.startCol]="--"
        self.board[move.endRow][move.endCol]=move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove=not self.whiteToMove
        #Update king's location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow,move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow,move.endCol)
        
        #Pawn Promotion
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol]=move.pieceMoved[0] + 'Q'
        
        #En passant
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--'
        
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow+move.endRow)//2,move.startCol)
        else:
            self.enpassantPossible=()
        #Castle 
        if move.isCastleMove:
            if move.endCol < move.startCol:  # Queen side castle
                self.board[move.endRow][0] = '--'
                self.board[move.endRow][move.endCol + 1] = move.pieceMoved[0] + 'R'
            else:  # King side castle
                self.board[move.endRow][7] = '--'
                self.board[move.endRow][move.endCol - 1] = move.pieceMoved[0] + 'R'


        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks,self.currentCastlingRight.bks,
                                           self.currentCastlingRight.wqs,self.currentCastlingRight.bqs))

    def undoMove(self):
        if len(self.moveLog)!=0:
            move=self.moveLog.pop()
            self.board[move.startRow][move.startCol]=move.pieceMoved
            self.board[move.endRow][move.endCol]=move.pieceCaptured
            self.whiteToMove= not self.whiteToMove
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow,move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow,move.startCol)
        #Undo En Passsant
        if move.isEnpassantMove:
            self.board[move.endRow][move.endCol]='--'
            self.board[move.startRow][move.endCol]=move.pieceCaptured
            self.enpassantPossible=(move.endRow,move.endCol)
        if move.pieceMoved[1] == 'P' and abs(move.startRow-move.endRow)==2:
            self.enpassantPossible = ()
        #Undo Castle Rights
        self.castleRightsLog.pop()
        self.currentCastlingRights.wks = self.castleRightsLog[-1].wks  # update current castling right
        self.currentCastlingRights.wqs = self.castleRightsLog[-1].wqs  # update current castling right
        self.currentCastlingRights.bks = self.castleRightsLog[-1].bks  # update current castling right
        self.currentCastlingRights.bqs = self.castleRightsLog[-1].bqs  # update current castling right
        if move.isCastleMove:
            if move.endCol < move.startCol:  # Queen Side Castle
                self.board[move.endRow][move.endCol + 1] = '--'
                self.board[move.endRow][0] = move.pieceMoved[0] + 'R'
            else:  # King side castle
                self.board[move.endRow][move.endCol - 1] = '--'
                self.board[move.endRow][7] = move.pieceMoved[0] + 'R'
        self.checkMate = False
        self.staleMate = False

    def updateCastleRights(self,move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks=False
            self.currentCastlingRight.wqs=False
        elif move.pieceMoved=='bK':
            self.currentCastlingRight.bks=False
            self.currentCastlingRight.bqs=False
        elif move.pieceMoved=='wR':
            if move.startRow==7:
                if move.startCol==0:
                    self.currentCastlingRight.wqs=False
                elif move.startCol==7:
                    self.currentCastlingRight.wks=False
        elif move.pieceMoved=='bR':
            if move.startRow==0:
                if move.startCol==0:
                    self.currentCastlingRight.bqs=False
                elif move.startCol==7:
                    self.currentCastlingRight.bks=False
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False
        
    def getValidMoves(self):
        tempCastlingRights = self.currentCastlingRight
        moves=[]
        self.inCheck,self.pins,self.checks=self.checkForPinsandChecks()
        if self.whiteToMove:
            kingRow=self.whiteKingLocation[0]
            kingCol=self.whiteKingLocation[1]
        else:
            kingRow=self.blackKingLocation[0]
            kingCol=self.blackKingLocation[1]
        if self.inCheck:
            if len(self.checks)==1:
                moves=self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow=check[0]
                checkCol=check[1]
                pieceChecking=self.board[checkRow][checkCol]
                validSquares=[]
                if pieceChecking[1]=='N':
                    validSquares=[(checkRow,checkCol)]
                else:
                    for i in range(1,8):
                        validSquare=(kingRow+check[2]*i,kingCol+check[3]*i)
                        validSquares.append(validSquare)
                        if validSquare[0]==checkRow and validSquare[1]==checkCol:
                            break
                for i in range(len(moves)-1,-1,-1):
                    if moves[i].pieceMoved[1]!='K':
                        if not(moves[i].endRow,moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:
                self.getKingMoves(kingRow,kingCol,moves)
        else:
            moves=self.getAllPossibleMoves()
        if len(moves) == 0:
            if self.inCheck:
                    self.checkMate=True
            else:
                self.staleMate=True
        else:
            self.staleMate=False
            self.checkMate=False
            
        self.currentCastlingRights=tempCastlingRights
        self.getCastleMoves(kingRow,kingCol,moves)
        return moves

    

    def getAllPossibleMoves(self):
        moves=[]
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn=self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves)
        return moves

    def getPawnMoves(self,r,c,moves):
        piecePinned= False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecePinned=True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        if self.whiteToMove:
            #Moves
            if self.board[r-1][c] == "--":
                if not piecePinned or pinDirection ==(-1,0):
                    moves.append(Move((r,c),(r-1,c),self.board))
                    if r == 6 and self.board[r-2][c] == "--":
                        moves.append(Move((r,c),(r-2,c),self.board))
            #Captures
            if c-1>=0:
                if self.board[r-1][c-1][0] == 'b':
                    if not piecePinned or pinDirection ==(-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board))
                elif (r-1,c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection ==(-1,-1):
                        moves.append(Move((r,c),(r-1,c-1),self.board,isEnpassantMove=True))

            if c+1<=7:
                if self.board[r-1][c+1][0] == 'b':
                    if not piecePinned or pinDirection ==(-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board))
                elif (r-1,c+1) == self.enpassantPossible:
                    if not piecePinned or pinDirection ==(-1,1):
                        moves.append(Move((r,c),(r-1,c+1),self.board,isEnpassantMove=True))

        else:
            if self.board[r+1][c] == "--":
                if not piecePinned or pinDirection ==(1,0):
                    moves.append(Move((r,c),(r+1,c),self.board))
                    if r == 1 and self.board[r+2][c] == "--":
                        moves.append(Move((r,c),(r+2,c),self.board))
            #Captures
            if c-1>=0:
                if self.board[r+1][c-1][0] == 'w':
                    if not piecePinned or pinDirection ==(1,-1):
                        moves.append(Move((r,c),(r+1,c-1),self.board))
                elif (r+1,c-1) == self.enpassantPossible:
                    if not piecePinned or pinDirection ==(1,-1):
                        moves.append(Move((r,c),(r+1,c-1),self.board,isEnpassantMove=True))

            if c+1<=7:
                if self.board[r+1][c+1][0] == 'w':
                    if not piecePinned or pinDirection ==(1,1):
                        moves.append(Move((r,c),(r+1,c+1),self.board))
                elif (r+1,c+1)== self.enpassantPossible:
                    if not piecePinned or pinDirection ==(1,1):
                        moves.append(Move((r,c),(r+1,c+1),self.board,isEnpassantMove=True))


    def getRookMoves(self,r,c,moves):
        piecePinned= False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecePinned=True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                if self.board[r][c][1]!='Q':
                    self.pins.remove(self.pins[i])
                break
        directions=((-1,0),(0,-1),(1,0),(0,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0 <= endRow<8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getKnightMoves(self,r,c,moves):
        piecePinned= False
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecePinned=True
                self.pins.remove(self.pins[i])
                break
        knightMoves=((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow=r+m[0]
            endCol=c+m[1]
            if 0 <= endRow<8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    

    def getBishopMoves(self,r,c,moves):
        piecePinned= False
        pinDirection=()
        for i in range(len(self.pins)-1,-1,-1):
            if self.pins[i][0]==r and self.pins[i][1]==c:
                piecePinned=True
                pinDirection=(self.pins[i][2],self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions=((-1,-1),(-1,1),(1,-1),(1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1,8):
                endRow=r+d[0]*i
                endCol=c+d[1]*i
                if 0 <= endRow<8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection==d or pinDirection==(-d[0],-d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r,c),(endRow,endCol),self.board))
                            break
                        else:
                            break
                else:
                    break

    def getQueenMoves(self,r,c,moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)
        

    def getKingMoves(self,r,c,moves):
        rowMoves=(-1,-1,-1,0,0,1,1,1)
        colMoves=(-1,0,1,-1,1,-1,0,1)
        allyColor="w" if self.whiteToMove else "b"
        for i in range(8):
            endRow=r+rowMoves[i]
            endCol=c+colMoves[i]
            if 0 <=endRow<8 and 0 <=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]!=allyColor:
                    if allyColor=='w':
                        self.whiteKingLocation=(endRow,endCol)
                    else:
                        self.blackKingLocation=(endRow,endCol)
                    inCheck,pins,checks=self.checkForPinsandChecks()
                    if not inCheck:
                        moves.append(Move((r,c),(endRow,endCol),self.board))
                    if allyColor=='w':
                        self.whiteKingLocation=(r,c)
                    else:
                        self.blackKingLocation=(r,c)
        

    def getCastleMoves(self,r,c,moves):
        if self.inCheck:
            return
        if (self.whiteToMove and self.currentCastlingRight.wks) or (not self.whiteToMove and self.currentCastlingRight.bks):
            self.getKingsideCastleMoves(r,c,moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r,c,moves)
    def getKingsideCastleMoves(self,r,c,moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2]=='--':
            if not self.isUnderAttack(r,c+1) and not self.isUnderAttack(r,c+2):
                moves.append(Move((r,c),(r,c+2),self.board,isCastleMove=True))

    def getQueensideCastleMoves(self,r,c,moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2]=='--' and self.board[r][c-3]=='--':
            if not self.isUnderAttack(r,c-1) and not self.isUnderAttack(r,c-2):
                moves.append(Move((r,c),(r,c-2),self.board,isCastleMove=True))
    
    def isUnderAttack(self, r, c):
        allyColor = 'w' if self.whiteToMove else 'b'
        enemyColor = 'b' if self.whiteToMove else 'w'
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        undetAttack = False
        for j in range(len(directions)):  # stands for direction => [0,3] -> orthogoal || [4,7] -> diagonal
            d = directions[j]
            for i in range(1, 8):  # stands for number of sq. away
                endRow = r + (d[0] * i)
                endCol = c + (d[1] * i)
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:
                        break
                    elif endPiece[0] == enemyColor:
                        pieceType = endPiece[1]
                        if (0 <= j <= 3 and pieceType == 'R') or \
                                (4 <= j <= 7 and pieceType == 'B') or \
								(i == 1 and pieceType == 'P') and (
								(enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5)) or \
								(pieceType == 'Q') or \
								(i == 1 and pieceType == 'K'):
                            return True
                        else:  # enemy piece not applying check
                            break
                else:  # OFF BOARD
                    break
        if undetAttack:
            return True
        knightMoves = [(-1, -2), (-2, -1), (1, -2), (2, -1), (1, 2), (2, 1), (-1, 2), (-2, 1)]
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow <= 7 and 0 <= endCol <= 7:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking king
                    return True
        return False
    def checkForPinsandChecks(self):
        pins=[]
        checks=[]
        inCheck=False
        if self.whiteToMove:
            enemyColor="b"
            allyColor="w"
            startRow=self.whiteKingLocation[0]
            startCol=self.whiteKingLocation[1]
        else:
            enemyColor="w"
            allyColor="b"
            startRow=self.blackKingLocation[0]
            startCol=self.blackKingLocation[1]
        directions=((-1,0),(0,-1),(1,0),(0,1),(-1,-1),(-1,1),(1,-1),(1,1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin=()
            for i in range(1,8):
                endRow=startRow+d[0]*i
                endCol=startCol+d[1]*i
                if 0 <= endRow < 8 and 0 <= endCol<8:
                    endPiece=self.board[endRow][endCol]
                    if endPiece[0]==allyColor and endPiece[1]!='K':
                        if possiblePin==():
                            possiblePin=(endRow,endCol,d[0],d[1])
                        else:
                            break
                    elif endPiece[0]==enemyColor:
                        type=endPiece[1]
                        if (9<=j<=3 and type=='R') or \
                                (4<=j<=7 and type=='B') or \
                                (i==1 and type=='P' and ((enemyColor=='w' and 6<=j<=7) or (enemyColor=='b'and 4<=j<=5))) or \
                                (type=='Q') or (i==1 and type=='K'):
                            if possiblePin == ():
                                inCheck=True
                                checks.append((endRow,endCol,d[0],d[1]))
                                break
                            else:
                                pins.append(possiblePin)
                                break
                        else:
                            break
                else:
                    break   
        knightMoves =((-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1))
        for m in knightMoves:
            endRow=startRow+m[0]
            endCol=startCol+m[1]
            if 0<=endRow<8 and 0<=endCol<8:
                endPiece=self.board[endRow][endCol]
                if endPiece[0]==enemyColor and endPiece[1]=='N':
                    inCheck=True
                    checks.append((endRow,endCol,m[0],m[1]))
        return inCheck,pins,checks
class CastleRights():
    def __init__(self,wks,bks,wqs,bqs):
        self.wks=wks
        self.bks=bks
        self.wqs=wqs
        self.bqs=bqs

class Move():
    ranksToRows={"1":7,"2":6,"3":5,"4":4,
                 "5":3,"6":2,"7":1,"8":0}
    rowsToRanks={v:k for k,v in ranksToRows.items()}
    filesToCols={"a":0,"b":1,"c":2,"d":3,
                 "e":4,"f":5,"g":6,"h":7}
    colsToFiles={v:k for k,v in filesToCols.items()}

    def __init__(self,startSqr,endSqr,board, isEnpassantMove=False,isCastleMove=False):
        self.startRow=startSqr[0]
        self.startCol=startSqr[1]
        self.endRow=endSqr[0]
        self.endCol=endSqr[1]
        self.pieceMoved=board[self.startRow][self.startCol]
        self.pieceCaptured=board[self.endRow][self.endCol]
        self.isPawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (self.pieceMoved == 'bP' and self.endRow == 7)
        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured= 'wP' if self.pieceMoved == 'bP' else 'bP'
        self.moveID=self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol 
        self.isCastleMove=isCastleMove
    #Overriding the equals method
    def __eq__(self,other):
        if isinstance(other,Move):
            return self.moveID==other.moveID
        return False
    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol) + self.getRankFile(self.endRow,self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c]+self.rowsToRanks[r]
        