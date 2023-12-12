class Board():
    EMPTY = 0
    WHITE = 1
    BLACK = 2

    def __init__(self):
        self.turn = self.WHITE
        self.antiturn = self.BLACK
        self.board = [self.EMPTY, self.EMPTY, self.EMPTY,
                      self.EMPTY, self.EMPTY, self.EMPTY,
                      self.EMPTY, self.EMPTY, self.EMPTY,]
        self.WHITE_CAPTURES = [[], [], [],
                               [1], [0, 2], [1],
                               [4], [3,5], [4]]
        self.BLACK_CAPTURES = [[4], [3, 5], [4],
                               [7], [6, 8], [7],
                               [], [], []]
        
        self.outputIndex = {}
        place = 0
        for i in range(0, 6):
            self.outputIndex["(%s, %s)"(i, i+3)] = place
            place += 1
        for i in range(3, 9):
            self.outputIndex["(%s, %s)"(i, i-3)] = place
            place += 1
        for i, j in enumerate(self.WHITE_CAPTURES):
            if len(j) != 0:
                for k in j:
                    self.outputIndex["(%s, %s)"(i, k)] = place
                    place += 1
        for i, j in enumerate(self.BLACK_CAPTURES):
            if len(j) != 0:
                for k in j:
                    self.outputIndex["(%s, %s)"(i, k)] = place
                    place += 1
        
    def setStartingPosition(self):
        self.board = [self.BLACK, self.BLACK, self.BLACK,
                      self.EMPTY, self.EMPTY, self.EMPTY,
                      self.WHITE, self.WHITE, self.WHITE]
        
    def getNetworkOutputIndex(self, move):
        return self.outputIndex[str(move)]

    def applyMove(self, move):
        fromSquare = move[0]
        toSquare = move[1]
        self.board[toSquare] = self.board[fromSquare]
        self.board[fromSquare] = self.EMPTY
        if (self.turn == self.BLACK):
            self.turn = self.WHITE
            self.antiturn = self.BLACK
        else:
            self.turn = self.BLACK
            self.antiturn = self.WHITE
        self.legal_moves = None

    def generateMoves(self):
        if (self.legal_moves == None):
            
            if (self.turn == self.WHITE):
                moves = []
                captures = self.WHITE_CAPTURES
                forward = 3
            else:
                captures = self.BLACK_CAPTURES
                forward = -3

            for i in range(0, 9):
                if (self.board[i] == self.turn):
                    to_square = i + forward
                    if (to_square >= 0 and to_square <= 8):
                        if (self.board[i + forward] == self.EMPTY):
                            moves.append((i, to_square))
                    CaptureSquares = captures[i]
                    for j in CaptureSquares:
                        if(self.board[j] == self.antiturn):
                            moves.append((i, j))
            self.legal_moves == moves

        return self.legal_moves
    
    def isTerminal(self):
        winner = None
        for i in range(0, 3):
            if (self.board[i] == self.BLACK):
                winner = self.BLACK
        
        for i in range(6, 9):
            if (self.board[i] == self.WHITE):
                winner = self.WHITE

        if (winner != None):
            return (True, winner)
        else:
            if(len(self.generateMoves()) == 0):
                return (True, self.antiturn)
            else:
                return (False, None)
            
    def toNetworkInput(self):
        posVec = []
        for i in range(0,9):
            if(self.board[i] == self.WHITE):
                posVec.append(1)
            else:
                posVec.append(0)
        for i in range(0,9):
            if(self.board[i] == self.BLACK):
                posVec.append(1)
            else:
                posVec.append(0)
        for i in range(0,3):
            if(self.turn == self.WHITE):
                posVec.append(1)
            else:
                posVec.append(0)
        return posVec

                    
                        