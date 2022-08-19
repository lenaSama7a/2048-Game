from random import random, choice
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)
directions = [LEFT, UP, RIGHT, DOWN]

class Board:

    def __init__(self, boardSize = 4):
        self.boardSize = boardSize
        self.board = [[0]*boardSize for i in range(boardSize)]
        self.score = 0
        self.addrandomTile()
        self.addrandomTile()
    def __str__(self):
        outStr = ''
        for i in self.board:
            outStr += '\t'.join(map(str,i))
            outStr += '\n'
        return outStr
    def __getitem__(self, key):
        return self.board[key]
    def getOpenTiles(self):
        openTiles = []
        for i in range(4): 
            for j in range(4): 
                if self.board[i][j] == 0:
                    openTiles.append((i,j))
        return openTiles

    def addrandomTile(self):
        openTiles = self.getOpenTiles()
        if len(openTiles) == 0: #if the board don't have any empty tile
            raise Exception("Unable to add tile, board is full")
        pos = choice(openTiles)
        if random() < 0.9:
            self.board[pos[0]][pos[1]]=2
        else:
            self.board[pos[0]][pos[1]]=4


    def addTile(self,m,n,tileToAdd, pos = None,h=0):
        if pos == None:
            openTiles = self.getOpenTiles()
            if len(openTiles) == 0: 
                raise Exception("Unable to add tile, board is full")
            self.board[m][n]=tileToAdd


    def Heuristic(self,x,y,newtile):     
        notaccepted = [[0,0,0,0], [0,0,0,0], [0,0,0,0],[0,0,0,0]]
        for i in range(4): 
            for j in range(4): 
                if self.board[i][j] == 2 or self.board[i][j]==4:
                    notaccepted[i][j]=self.board[i][j]
        h=1
        for i in range(4):
            if notaccepted[x][i]==newtile:
                h=5
                break
            else:
                for j in range(4):
                    if notaccepted[j][y]==newtile:
                     h=5
                     break
    
        return h

    def minmaxToAddTile(self):
        openTiles = self.getOpenTiles()
        if random() < 0.9:
            Heuristic= [[0,0,0,0], [0,0,0,0], [0,0,0,0],[0,0,0,0]]
            for x,y in openTiles: 
                Heuristic[x][y]=self.Heuristic(x,y,2)               
            
            for i in range(4):
                for j in range(4):
                    if Heuristic[i][j]==5:
                        f=i
                        s=j
            for i in range(4):
                for j in range(4):
                    if Heuristic[i][j]==1:
                        f=i
                        s=j
                        
            self.addTile(f,s,2)   
        else:
            Heuristic= [[0,0,0,0], [0,0,0,0], [0,0,0,0],[0,0,0,0]]
            for x,y in openTiles: #{(0,0),(0,1)....}
                Heuristic[x][y]=self.Heuristic(x,y,4)
                
            
            for i in range(4):
                for j in range(4):
                    if Heuristic[i][j]==5:
                        f=i
                        s=j
            for i in range(4):
                for j in range(4):
                    if Heuristic[i][j]==1:
                        f=i
                        s=j
                        
            self.addTile(f,s,4)

    def move(self,dir,addNextTile=True):
        hadCollision = [[False]*self.boardSize for i in range(self.boardSize)] #4*4 false values
        hadMovement = False
        score = 0

        xStart = 0
        xEnd = self.boardSize
        if dir[1] > 0:
            xStart = self.boardSize - 1
            xEnd = -1

        yStart = 0
        yEnd = self.boardSize
        if dir[0] > 0:
            yStart = self.boardSize - 1
            yEnd = -1
        for y in range(yStart, yEnd, -dir[0] if dir[0] != 0 else 1):
            for x in range(xStart, xEnd, -dir[1] if dir[1] != 0 else 1):
                if self.board[y][x] == 0:
                    continue

                yCheck = y + dir[0]
                xCheck = x + dir[1]

                while yCheck >= 0 and yCheck < self.boardSize \
                    and xCheck >= 0 and xCheck < self.boardSize \
                    and self.board[yCheck][xCheck] == 0:
                    yCheck += dir[0]
                    xCheck += dir[1]
                # Move back if we went out of bounds
                if yCheck < 0 or yCheck >= self.boardSize \
                    or xCheck < 0 or xCheck >= self.boardSize:
                    yCheck -= dir[0]
                    xCheck -= dir[1]
                # If no movement, break
                if yCheck == y and xCheck == x:
                    continue
                elif self.board[y][x] == self.board[yCheck][xCheck] and not hadCollision[yCheck][xCheck]:
                    # else If Equal and not combined already, combine
                    hadCollision[yCheck][xCheck] = True 
                    hadMovement = True 
                    self.board[yCheck][xCheck] += self.board[y][x]
                    score += self.board[yCheck][xCheck] 
                    self.board[y][x] = 0
                elif self.board[yCheck][xCheck] == 0:
                    # else if movement into empty tile, simply move
                    hadMovement = True
                    self.board[yCheck][xCheck] = self.board[y][x]
                    self.board[y][x] = 0
                else:
                    # Else, move back
                    yCheck -= dir[0]
                    xCheck -= dir[1]
                    if yCheck == y and xCheck == x:
                        continue
                    hadMovement = True
                    temp = self.board[y][x]
                    self.board[y][x] = 0
                    self.board[yCheck][xCheck] = temp
        self.score += score
        if hadMovement and addNextTile:
            self.minmaxToAddTile()
        return score, hadMovement

    # Returns True if no legal moves exist
    def checkLoss(self):
        for y in range(self.boardSize): 
            for x in range(self.boardSize):
                if self.board[y][x] == 0:
                    return False
                for dir in directions:
                    if y + dir[0] >= 0 and y + dir[0] < self.boardSize \
                        and x + dir[1] >= 0 and x + dir[1] < self.boardSize \
                        and self.board[y][x] == self.board[y+dir[0]][x+dir[1]]:
                        return False
        return True
