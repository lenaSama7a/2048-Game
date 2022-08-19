import sys, pygame 
import model
import multiprocessing as mp

size = width, height = 480, 500
playRegion = 480, 480

# Colors
black = (0,0,0)
white = (255,255,255)
fontColor = (75,00,130)  #dark blue
defaultTileColor = (232,232,232) #light grey
tileBoarderColor = fontColor

# Game
boardSize = 4
def drawBoard(screen, board):
    screen.fill(black)
    for i in range(board.boardSize):
        for j in range(board.boardSize):
            color = defaultTileColor
            numberText = '' 
            if board.board[i][j] == 2:
                color = (255,255,224)  
                numberText = str(board.board[i][j])
            elif board.board[i][j] == 4:
                color = (255,222,173)
                numberText = str(board.board[i][j])
            elif board.board[i][j] == 8:
                color = (255,165,79)
                numberText = str(board.board[i][j])
            elif board.board[i][j] == 16:
                color = (238,149,114)
                numberText = str(board.board[i][j])
            elif board.board[i][j] == 32:
                color = (240,128,128)
                numberText = str(board.board[i][j])
            elif board.board[i][j] == 64:
                color = (255,99,71)
                numberText = str(board.board[i][j])
            elif board.board[i][j] == 128:
                color = (227,207,87)
                numberText = str(board.board[i][j])  
            elif board.board[i][j] == 256 or board.board[i][j] == 512 or board.board[i][j] == 1024:
                color = (255,215,0)
                numberText = str(board.board[i][j])
            elif board.board[i][j] == 2048:
                color = (255,174,185)
                numberText = str(board.board[i][j]) 
            

            #Rect(left, top, width, height)   
            rect = pygame.Rect(j*480/4,
                                i*480/4,
                                480/4,
                                480/4)
            pygame.draw.rect(screen, color, rect) #function to draw rectangle with specific color
            pygame.draw.rect(screen, fontColor, rect, 1) #to draw borders around tiles with thickness=1
            #font.render: draw text on a new Surface
            fontImage = tileFont.render(numberText, 0, fontColor)
            screen.blit(fontImage,
                    (j*480/4 + (480/4 - fontImage.get_width())/2,
                    i*480/4 + (480/4 - fontImage.get_height())/2))
    fontImage = scoreFont.render("Score: {:,}".format(board.score), 1, white)
    screen.blit(fontImage, (1, 481))

    if board.checkLoss() :
        s = pygame.Surface((480, 480), pygame.SRCALPHA)
        s.fill([238, 228, 218, 200])
        screen.blit(s, (0, 0))
        msg1 = "GAME OVER!!"
        msg2= "YOUR SCORE is: " 
        msg3= str(board.score)
        screen.blit(tileFont.render(msg1, 1, (255,64,64)), (80, 130))
        screen.blit(tileFont.render(msg2, 1, (255,64,64)), (40, 200))
        screen.blit(tileFont.render(msg3, 1, (255,64,64)), (200, 270))
        pygame.display.update()

def handleInput(event, board):
    if event.type == pygame.QUIT: 
            pool.close()
            pool.terminate()
            sys.exit() #exit Python interpreter 
    if event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_RIGHT:
            board.move(model.RIGHT)
        elif event.key == pygame.K_LEFT:
            board.move(model.LEFT)
        elif event.key == pygame.K_UP:
            board.move(model.UP)
        elif event.key == pygame.K_DOWN:
            board.move(model.DOWN)
        elif event.key == pygame.K_ESCAPE:
            pool.close()
            pool.terminate()
            sys.exit()

    return board

def gameLoop():
    board = model.Board(boardSize)
    while 1:
        for event in pygame.event.get(): #get events , events: clicks
            board = handleInput(event, board) #we built this function above
        
        drawBoard(screen, board) 
        pygame.display.flip() #display screen      

if __name__ == '__main__': 
    global screen
    global tileFont
    global scoreFont
    global pool
    mp.freeze_support()
    mp.set_start_method('spawn')
    pool = mp.Pool(processes=4) 
    pygame.init() 
    screen = pygame.display.set_mode(size) 
    pygame.display.set_caption("2048 Lena And Shahd")
    tileFont = pygame.font.SysFont("classic-roman", 72) 
    scoreFont = pygame.font.SysFont("", 22)
    gameLoop()
