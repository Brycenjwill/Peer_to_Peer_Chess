"""
Welcome to my chess program!

Here is a link to the spritework that I used... https://opengameart.org/content/chess-pieces-and-board-squares
"""
import threading
import socket
import pygame
import time

#GLOBAL CONSTANTS
running = True
WIDTH = 500
HEIGHT = 600
WHITE = pygame.Color("#F8F9FA")
BLACK = pygame.Color("#212529")
GREEN = pygame.Color("#ADB5BD")
TAN = pygame.Color("#6C757D")

SERVERIP = 'IP'#Set this IP before running.

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
xaxisList = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] #From left to right
yaxisList = [8, 7, 6, 5, 4, 3, 2, 1] #From top to bottom
kings = []
blackBorder = []
whiteBorder = []
allPossibleMoves = []
coordinants = []
check = False
font = pygame.font.Font('freesansbold.ttf', 32)
menuFont = pygame.font.Font('freesansbold.ttf', 70)
winner = 3 #Set winner as 3 for logic


#Class for all board squares, used for mouse tracking and display
class Square:
    def __init__(self, color, locationx, locationy, xaxis, yaxis):
        self.locationx = locationx
        self.locationy = locationy
        self.color = color
        self.beginColor = color
        self.xaxis = xaxis #Xaxis and Yaxis values are for deciding if moves are legal later on
        self.yaxis = yaxis
        #occupied and piece are for tracking who is in said space.
        self.occupied = False
        self.piece = None #Contains a pointer to the object that is in this square
        self.selected = False

    def getPos(self):
        return self.locationx, self.locationy
    
    def getColor(self):
        return self.color
    
    def hover(self):
        #Set hover color
        self.color = GREEN

    def resetColor(self): 
        #Reset color to initial color when not hovering
        if self.selected == True:
            self.color = GREEN
        else:
            self.color = self.beginColor

    def setPiece(self, piece):
        self.piece = piece
        self.occupied = True

    def getPiece(self):
        return self.piece

    def getAxis(self):
        return self.xaxis,self.yaxis

    def getOccupied(self):
        return self.occupied
    
    def select(self):
        self.selected = True
    def unselect(self):
        self.selected = False
    def getSelected(self): #Get whether the square is selected
        return self.selected
    def setPossible(self):
        self.possible = True
    def resetPossible(self):
        self.possible = False
    def removePiece(self):
        self.occupied = False
        self.piece = None

class Piece:
    def __init__(self, square, type, team, image):
        self.square = square
        self.type = type
        self.team = team
        self.image = pygame.image.load(image)
        self.firstMove = True
        self.alive = True

    def setSquare(self, newSquare): #Move to new square
        self.square = newSquare


    def getTeam(self):
        return self.team
    
    def getType(self):
        return self.type

    def die(self): #Unlink the piece from the square
        self.square = None
        self.alive = False

    def getAlive(self):
        return self.alive

    def getImage(self):
        return self.image

    def getSquare(self):
        return self.square
    
    def pawnMoved(self):
        self.firstMove = False
    #For pawns, gets if the pawn hasn't moved yet
    def getFirst(self):
        return self.firstMove

#Get the sqaures on the border of a king, for finding check mates
def kingBorder(team):
    border = []
    index = None
    king = kings[team]
    ksquare = king.getSquare()
    for i, square in enumerate(squares):
        if square == ksquare:
            index = i

    if ksquare.getAxis()[0] != "H":
        border.append(squares[index + 1])
        if ksquare.getAxis()[1] != 8:
            border.append(squares[index -7])
        if ksquare.getAxis()[1] != 1:
            border.append(squares[index + 9])
    if ksquare.getAxis()[0] != "A":
        border.append(squares[index - 1])
        if ksquare.getAxis()[1] != 8:
            border.append(squares[index - 9])
        if ksquare.getAxis()[1] != 1:
            border.append(squares[index + 7])
    if ksquare.getAxis()[1] != 8:
        border.append(squares[index - 8])
    if ksquare.getAxis()[1] != 1:
        border.append(squares[index + 8])
    return border

#Init all of the square objects for the board
def initSquares():
    squares = []
    
    row = 0
    column = 0
    posx = 50
    posy = 100
    for i in range(64): 
            if row % 2 == 0:
                if i % 2 == 0:
                    color = WHITE
                else: 
                    color = BLACK
            else:
                if i % 2 == 0:
                    color = BLACK
                else: 
                    color = WHITE
            
            square = Square(color, posx, posy, xaxisList[column], yaxisList[row]) #Create Square
            squares.append(square)

            if posx == 400:
                posy += 50
                posx = 50
                row += 1
                column = 0
            else:
                posx += 50
                column += 1
    return squares
#Gets axis indexes for square, returns x, y indexes
def getAxis(xaxis, yaxis):
    for index, axis in enumerate(xaxisList):
        if axis == xaxis:
            xindex = index
    for index, axis in enumerate(yaxisList):
        if axis == yaxis:
            yindex = index
    return xindex, yindex

#Init all pieces for the board and assign them to squares
def initPieces(squares):
    types = [0,1,2,3,4,2,1,0,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,0,1,2,3,4,2,1,0,] 
    pieces = []
    squareIndex = 0

    #Set all attributes for starting pieces
    for i in range(32):
        king = False
        if i < 16:
            team = 0 #Team 0 is Black
        else:
            team = 1 #Team 1 is White
            squareIndex = i + 32

        if types[i] == 0: #Rooks
            if team == 0:
                sprite = "sprites\\b_rook_png_128px.png"
            else:
                sprite = "sprites\\w_rook_png_128px.png"        
        elif types[i] == 1: #Knights
            if team == 0:
                sprite = "sprites\\b_knight_png_128px.png"
            else:
                sprite = "sprites\\w_knight_png_128px.png"
        elif types[i] == 2: #Bishops
            if team == 0:
                sprite = "sprites\\b_bishop_png_128px.png"
            else:
                sprite = "sprites\\w_bishop_png_128px.png"
        elif types[i] == 3: #Queens
            if team == 0:
                sprite = "sprites\\b_queen_png_128px.png"
            else:
                sprite = "sprites\\w_queen_png_128px.png"
        elif types[i] == 4: #King
            if team == 0:
                sprite = "sprites\\b_king_png_128px.png"
                king = True
            else:
                sprite = "sprites\\w_king_png_128px.png"
                king = True
        elif types[i] == 5: #Pawns
            if team == 0:
                sprite = "sprites\\b_pawn_png_128px.png"

            else:
                sprite = "sprites\\w_pawn_png_128px.png"

        piece = Piece(squares[squareIndex], types[i], team, sprite) 
        pieces.append(piece) #Add piece to list of pieces to return
        piece.getSquare().setPiece(piece) #Assign piece to square location within square object that is holding the piece
        if king == True:
            kings.append(piece)
            king = False
        squareIndex += 1
    return pieces
#Handle move decision for any pawn piece
def pawnMovement(possibleMoves, team, squares, square, i):
    targeted = []
    if team == 1: #Set direction pawn can move in on the y axis.
        direction = -1
    else:
        direction = 1

    xaxis = square.getAxis()[0] #Get the board location of the piece
    
    yaxis = square.getAxis()[1]
    firstMove = square.getPiece().getFirst()
    #Gets the index of x and y axis in yaxislist and xaxislist
    xy = getAxis(xaxis, yaxis)
    #Variable for deciding if a pawn can move 2 at once.
    blocked = True
    #look through squares list for possible moves

    #Moving straight forward. . .
    inFront = squares[i + (8*direction)]
    if inFront.getOccupied() == False: #Check if the piece in front is occupied
        targeted.append(inFront)
        if square.getPiece().getFirst() == True: #Check if this is the pawns first move...
            doubleStep = squares[i + (16 *direction)] #Check if two pieces in front is occupied
            if doubleStep.getOccupied() == False:
                targeted.append(doubleStep)
   #Killing another piece. . .
    diagList = []
    corner = []
    if xaxis != 'A' and xaxis != "H": #Make sure that each team does not attempt to attack off the board, respectively
        diagList.append(squares[i + (7*direction)])
        diagList.append(squares[i + (9*direction)])
    elif xaxis == 'A':
        if team == 1:
            diagList.append(squares[i + (7*direction)])
        else:
            diagList.append(squares[i + (9*direction)])
    elif xaxis == "H":
        if team == 0:
            diagList.append(squares[i + (7*direction)])
        else:
            diagList.append(squares[i + (9*direction)])

    for square in diagList:
        if square.getOccupied() == True:
            if square.getPiece().getTeam() != team:
                targeted.append(square)
        corner.append(square)
    return targeted, corner

#Handle move decision for any rook piece
def rookMovement(possibleMoves, team, squares, square, i):
    """
    Casle rules: Can move in any direction as long as it isnt diaganal or blocked by a piece.
    """
    #Check four directions in order.
    targeted = []
    xaxis = square.getAxis()[0] #Get the board location of the piece
    yaxis = square.getAxis()[1]

    #Check upward movement. . . 
    upY = i
    #Make sure piece isn't on top before checking if it can move upwards
    if squares[i].getAxis()[1] != 8:
        while True:
            if squares[upY - 8].getOccupied() == False:
                targeted.append(squares[upY - (8)])
                if squares[upY - 8].getAxis()[1] == 8:
                    break
                upY = upY - 8
            else:
                if squares[upY - (8)].getPiece().getTeam() != team:
                    targeted.append(squares[upY - (8)])
                break
            

    #Check Downward Movement
    downY = i
    if squares[i].getAxis()[1] != 1:
            while True:
                if squares[downY + (8)].getOccupied() == False:
                    targeted.append(squares[downY + (8)])
                    if squares[downY + 8].getAxis()[1] == 1:
                        break
                    downY = downY + 8
                else:
                    if squares[downY + (8)].getPiece().getTeam() != team:
                        targeted.append(squares[downY + (8)])
                    break

    rightX = i
    if squares[i].getAxis()[0] != "H":
            while True:
                if squares[rightX + (1)].getOccupied() == False:
                    targeted.append(squares[rightX + (1)])
                    if squares[rightX + 1].getAxis()[0] == "H":
                        break
                    rightX = rightX + 1
                else:
                    if squares[rightX + (1)].getPiece().getTeam() != team:
                        targeted.append(squares[rightX + (1)])
                    break
    leftX = i
    if squares[i].getAxis()[0] != "A":
            while True:
                if squares[leftX - 1].getOccupied() == False:
                    targeted.append(squares[leftX - (1)])
                    if squares[leftX - 1].getAxis()[0] == "A": #Stop if on the edge you are moving towards
                        break
                    leftX = leftX - 1
                else:
                    if squares[leftX - 1].getPiece().getTeam() != team:
                        targeted.append(squares[leftX - 1])
                    break
    return targeted
#Handle move decisions for any bishop piece
def bishopMovement(possibleMoves, team, squares, square, i):
    #Check four directions in order.
    targeted = []
    blocked = [] #For checking check mate and check
    xaxis = square.getAxis()[0] #Get the board location of the piece
    yaxis = square.getAxis()[1]
#First, check upwards
    if yaxis != 8:
        if xaxis != "H": #Make sure there is space to the right of bishop
            updex = i
            #Try to move up to the right
            while True:
                if squares[updex - 7].getOccupied() == False:
                    targeted.append(squares[updex - 7])
                    if squares[updex - 7].getAxis()[0] != "H" and squares[updex - 7].getAxis()[1] != 8:
                        updex = updex - 7
                    else:
                        break
                else:
                    if squares[updex - 7].getPiece().getTeam() != team:
                        targeted.append(squares[updex - 7])
                    break
            #Try to move up to the left
        if xaxis != "A":
            updex = i #Reset index
            while True:
                if squares[updex - 9].getOccupied() == False:
                    targeted.append(squares[updex - 9])
                    if squares[updex - 9].getAxis()[0] != "A" and squares[updex - 7].getAxis()[1] != 8:
                        updex = updex - 9
                    else:
                        break
                else:
                    if squares[updex - 9].getPiece().getTeam() != team:
                        targeted.append(squares[updex - 9])
                    break
#Last, check downwards
    if yaxis != 1:
        if xaxis != "H": #Make sure there is space to the right of bishop
            downdex = i
            #Try to move down to the right
            while True:
                if squares[downdex + 9].getOccupied() == False:
                    targeted.append(squares[downdex + 9])
                    if squares[downdex + 9].getAxis()[0] != "H" and squares[downdex + 9].getAxis()[1] != 1:
                        downdex = downdex + 9
                    else:
                        break
                else:
                    if squares[downdex + 9].getPiece().getTeam() != team:
                        targeted.append(squares[downdex + 9])
                    break
            #Try to move down to the left
        if xaxis != "A":
            downdex = i #Reset index
            while True:
                if squares[downdex + 7].getOccupied() == False:
                    targeted.append(squares[downdex + 7])
                    if squares[downdex + 7].getAxis()[0] != "A" and squares[downdex + 7].getAxis()[1] != 1:
                        downdex = downdex + 7
                    else:
                        break
                else:
                    if squares[downdex + 7].getPiece().getTeam() != team:
                        targeted.append(squares[downdex + 7])
                    break
    return targeted
#Handle move decision for any knight piece
def knightMovement(possibleMoves, team, squares, square, i):
    targeted = []
    xaxis = square.getAxis()[0] #Get the board location of the piece that will move
    yaxis = square.getAxis()[1]

    piece = square.getPiece()

#First, try to go 2 upwards. . . 
    #Make sure piece is not on the top edge. . .
    if yaxis != 7 and yaxis != 8:
        #Make sure piece is not on left edge. . .
        if xaxis != "A":
            if squares[i - 17].getOccupied() == False:
               targeted.append(squares[i - 17])
            else:
                #Add to possible moves if piece in location is on the other team
                if squares[i - 17].getPiece().getTeam() != team:
                    targeted.append(squares[i - 17])
        #Make sure piece is not on right edge. . .
        if xaxis != "H":
            if squares[i - 15].getOccupied() == False:
               targeted.append(squares[i - 15])
            else:
                #Add to possible moves if piece in location is on the other team
                if squares[i - 15].getPiece().getTeam() != team:
                    targeted.append(squares[i - 15])
#Next, try to go 2 downwards. . . 
    #Make sure piece is not on the top edge. . .
    if yaxis != 1 and yaxis != 2:
        #Make sure piece is not on right edge. . .
        if xaxis != "H":
            if squares[i + 17].getOccupied() == False:
               targeted.append(squares[i + 17])
            else:
                #Add to possible moves if piece in location is on the other team
                if squares[i + 17].getPiece().getTeam() != team:
                    targeted.append(squares[i + 17])
        #Make sure piece is not on left edge. . .
        if xaxis != "A":
            if squares[i + 15].getOccupied() == False:
               targeted.append(squares[i + 15])
            else:
                #Add to possible moves if piece in location is on the other team
                if squares[i + 15].getPiece().getTeam() != team:
                    targeted.append(squares[i + 15])
#Next, try to go 1 upwards. . .
    if yaxis != 8: #Try to go left
        if xaxis != "A" != xaxis != "B":
            if squares[i - 10].getOccupied() == False:
                targeted.append(squares[i - 10])
            else:
                if squares[i - 10].getPiece().getTeam() != team:
                    targeted.append(squares[i - 10])
        if xaxis != "G" != xaxis != "H": #Try to go right
            if squares[i - 6].getOccupied() == False:
                targeted.append(squares[i - 6])
            else:
                if squares[i - 6].getPiece().getTeam() != team:
                    targeted.append(squares[i - 6])
#Next, try to go 1 downwards. . .
    if yaxis != 1: #Try to go left
        if xaxis != "A" != xaxis != "B":
            if squares[i + 6].getOccupied() == False:
                targeted.append(squares[i + 6])
            else:
                if squares[i + 6].getPiece().getTeam() != team:
                    targeted.append(squares[i + 6])
        if xaxis != "G" != xaxis != "H": #Try to go right
            if squares[i + 10].getOccupied() == False:
                targeted.append(squares[i + 10])
            else:
                if squares[i + 10].getPiece().getTeam() != team:
                    targeted.append(squares[i + 10])
    return targeted

def kingMovement(possibleMoves, team, squares, square, i):
    possible = []
    cheatBorder = []
    border = kingBorder(team)
    for square in border:
        cheatBorder.append(square) #Kings can never come within 1 of each other, this is a fix for that
        if square not in allPossibleMoves:
            if square.getOccupied() == False:
                possible.append(square)
            else:
                if square.getPiece().getTeam() != team:
                    possible.append(square)
    return possible, cheatBorder

def checkPossible(checking):
    possible = []
    if storedSquares[0] != 0: #Make sure there is a square/piece selected
            currentPlayer = checking
            selectedPiece = storedSquares[0].getPiece()
            pieceType = selectedPiece.getType()
            #Get all possible for rooks. . . 
            if pieceType == 0:
                possible = rookMovement(possibleMoves, currentPlayer, squares, storedSquares[0], squaredex)
            #Get all possible for knights. . . 
            if pieceType == 1:
                possible = knightMovement(possibleMoves, currentPlayer, squares, storedSquares[0], squaredex)
            #Get all possible for bishops
            if pieceType == 2:
                possible = bishopMovement(possibleMoves, currentPlayer, squares, storedSquares[0], squaredex)
            #Get all possible for queens. . .
            if pieceType == 3:
                possible = rookMovement(possibleMoves, currentPlayer, squares, storedSquares[0], squaredex) +bishopMovement(possibleMoves, currentPlayer, squares, storedSquares[0], squaredex)
            #Get all possible for Kings. . .
            if pieceType == 4:
                possible = kingMovement(possibleMoves, currentPlayer, squares, storedSquares[0], squaredex)[0]
            #Get possible pieces for Pawns. . . 
            if pieceType == 5:
                possible = pawnMovement(possibleMoves, currentPlayer, squares, storedSquares[0], squaredex)[0]
    return possible

def getAllPossible(checking):
    possible = []
    
    for i, square in enumerate(squares): #Go through all pieces on opposite team to get all possible attacking list
            if square.getOccupied() == True:
                if square.getPiece().getTeam() == checking:
                    selectedPiece = square.getPiece()
                    pieceType = selectedPiece.getType()
                    #Get all possible for rooks. . . 
                    if pieceType == 0:
                        temp = rookMovement(possibleMoves, checking, squares, square, i)
                    #Get all possible for knights. . . 
                    if pieceType == 1:
                        temp = knightMovement(possibleMoves, checking, squares, square,i)
                    #Get all possible for bishops
                    if pieceType == 2:
                        temp = bishopMovement(possibleMoves, checking, squares, square,i)
                    #Get all possible for queens. . .
                    if pieceType == 3:
                        temp = rookMovement(possibleMoves, checking, squares, square,i) +bishopMovement(possibleMoves, checking, squares, square,i)
                    #Get all possible for kings. . .
                    if pieceType == 4:
                        temp = kingMovement(possibleMoves, checking, squares, square, i)[1]
                    #Get possible pieces for Pawns. . . 
                    if pieceType == 5:
                        temp = pawnMovement(possibleMoves, checking, squares, square,i)[1]
                    possible = possible + temp
    return possible
  
def switchTeams(currentTeam):
    if currentTeam == 1:
        return 0
    else:
        return 1

#Handles reassignment of piece when moved and removal of piece that will be "Killed"
def movepiece(currentSquare, futureSquare):
    currentPiece = currentSquare.getPiece() #The piece that will be moving
    if futureSquare.getOccupied() == True:
        toKill = futureSquare.getPiece()
        toKill.die() #Kill piece (remove from board)
    currentPiece.setSquare(futureSquare) #Assign the new square to the piece for drawing
    futureSquare.setPiece(currentPiece) #Assign piece to square for logic
    currentSquare.removePiece()
    currentPiece.pawnMoved()

def getCheck(team, allPossibleMoves):
    if kings[team].getSquare() in allPossibleMoves:
        check = True
    else:
        check = False
    return check
    
def getCheckMate(check, possibleMoves):
    if len(possibleMoves) == 0:
        if check == True:
            return True
    else:
        return False

#Function for connecting to server
def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVERIP, 9999)) #Connect to the server
    print("Connected")
    return client

#Setting global lists
squares = initSquares() #squares is where all the squares are stored in a list
pieces = initPieces(squares) #This is where all of the pieces are stored.
storedSquares = [0] #A list with the currently selected square and the previously selected square.
possibleMoves = []
currentPlayer = 1 #sets starting player, 1 is white to start, 0 is black.
squaredex = None #Index of currently selected square


#Start listener client. . .
#Define listener here
Started = False

#This section is the main menu, on start it will ask the player if they will host or join a game.
while Started == False:
    welcome = font.render(f'Welcome to my program!', True, WHITE, BLACK)
    mainMenuHost = menuFont.render(f'HOST', True, WHITE, BLACK)
    mainMenuJoin = menuFont.render(f'JOIN', True, WHITE, BLACK)
    joinRect = mainMenuJoin.get_rect(topleft=(167,400))
    hostRect = mainMenuHost.get_rect(topleft=(150,300))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Started = True
    if hostRect.collidepoint(pygame.mouse.get_pos()):  #For if you will be hosting
        if  event.type == pygame.MOUSEBUTTONUP:
            print("Hosting the game")
            #TO DO: CONNECT AS HOST/WHITE
            Player = 1
            Started = True
            client = connect()

    elif joinRect.collidepoint(pygame.mouse.get_pos()):  #For if you will be joining
        if  event.type == pygame.MOUSEBUTTONUP:
            print("Joining a game")
            #TO DO: CONNECT AS BLACK/2ND PLAYER
            Player = 0
            Started = True
            client = connect()

    screen.fill(GREEN)
    screen.blit(welcome, (50, 100))

    screen.blit(mainMenuHost, hostRect)
    screen.blit(mainMenuJoin, joinRect)
    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

def clientSend(square1, square2):
    message = f"{square1.getAxis()},,,{square2.getAxis()}"
    client.send(message.encode('utf-8')) #Send coordinants to other player

def clientRecieve(coordinants):
     while True:
        try:
            message = client.recv(1024).decode() #Get message from other player
            msgSplit = message.split(",,,")
            coordinants.append(msgSplit)
            print("Got message")
            print(coordinants)
        except:
            client.close()
            break

thread = threading.Thread(target=clientRecieve, args=(coordinants,))
thread.start()

#Start Progam. . . 
while running:

    if winner != 3:
        time.sleep(2)
        thread.join()
        pygame.quit()
        break

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            thread.join()
            pygame.quit()

    #This section is used to select squares and move pieces.
    #Make sure the turn is the current player, so that you can only move pieces on your turn.
    for i, square in enumerate(squares):
        squareRect = pygame.Rect(square.getPos()[0], square.getPos()[1], 50, 50)
        #Check if mouse over square
        if squareRect.collidepoint(pygame.mouse.get_pos()):   
                if event.type == pygame.MOUSEBUTTONDOWN:

                    #time.sleep(.1) #Wait to avoid multiclick, this is chess after all
                    #Check if the square you are mousing over is movable. . 
                    if storedSquares[0] != 0:
                            if square in possibleMoves:
                                movepiece(storedSquares[0], square)
                                clientSend(storedSquares[0], square) #Send coordinants to other player. . .
                                for square in squares: #Reset all board colors
                                    square.unselect()
                                storedSquares = [0]
                                possibleMoves = [] #Reset possible moves
                                currentPlayer = switchTeams(currentPlayer)


                    if storedSquares[0] != 0: #if there is already a square selected
                        if Player == currentPlayer:
                            if square.getOccupied() == True:
                                if square.getPiece().getTeam() == Player:
                                    selectedSquare = square #Maybe store the square you last hovered on?
                                    storedSquares.append(storedSquares[0]) #last square clicked on
                                    storedSquares[0] = selectedSquare
                                    squaredex = i #Save index of selected square
                                    possibleMoves = []
                    else: #first time selecting a piece per turn
                        if Player == currentPlayer:
                            if square.getOccupied() == True:
                                if square.getPiece().getTeam() == Player:
                                    storedSquares[0] = square #For first click
                                    squaredex = i #Save index of selected square

                    if storedSquares[0] != 0:
                        storedSquares[0].select()
                    if len(storedSquares) > 1: #if there are two stored squares, one selected and one to unselect
                        storedSquares[1].unselect()
                        storedSquares.pop() #forget about old stored square
        else:
            #Reset color once no longer hovering over square, or once a square is no longer selected.
            square.resetColor()
            if check == True:
                if checkMarkRect.collidepoint(pygame.mouse.get_pos()):
                    if  event.type == pygame.MOUSEBUTTONDOWN:
                        winner = switchTeams(currentPlayer)


    
    if Player != currentPlayer: #if the current player is waiting for a result. . .
        storedSquares = [0]
        if len(coordinants) != 0: #This means that the client has recieved info from the server.
            #TODO: Once you get the coordinants back from the other player, change the 
            #current player, and move pieces on this client. 
            print(f"0 {coordinants[0][0]}")
            print(f"1 {coordinants[0][1]}")
            for square in squares:
                print(square.getAxis())
                if str(square.getAxis()) == coordinants[0][0]:
                    square1 = square
                elif str(square.getAxis()) == coordinants[0][1]:
                    square2 = square
            coordinants.clear() #Reset coordinants list
            movepiece(square1, square2) #Move pieces on this clients end
            currentPlayer = switchTeams(currentPlayer) #Switch current player

    #Run through piece types, get list of possible moves/squares (possibleMoves)

    possibleMoves = checkPossible(currentPlayer)
    
    checking = switchTeams(currentPlayer)
    allPossibleMoves = getAllPossible(checking)
    check = getCheck(currentPlayer, allPossibleMoves)

    #Set colors for possible moves, remove after testing is complete!!!
    for square in possibleMoves:
        square.hover()


    # fill the screen with a color to wipe away anything from last frame
    screen.fill(TAN)

    #Draw board squares
    for square in squares:
        pygame.draw.rect(screen, square.getColor(), pygame.Rect(square.getPos()[0], square.getPos()[1], 50, 50))

    for piece in pieces:
        if piece.getAlive() == True:
            screen.blit(piece.getImage(), (piece.getSquare().getPos()[0], piece.getSquare().getPos()[1]))

    if winner != 3:
        if winner == 1:
            winner = "White"
        else:
            winner = "Black"
        winnerDisplay = font.render(f'{winner} wins!', True, WHITE, BLACK)
        screen.blit(winnerDisplay, (160, 530))
        check = False
        time.sleep(1)
        pygame.quit()

    if check == True:
        checkmateDisplay = font.render(f'Checkmate?', True, WHITE, BLACK)
        screen.blit(checkmateDisplay, (230, 565))
        checkMark = font.render('[X]', True, WHITE, BLACK)
        checkMarkRect = checkMark.get_rect(topleft=(445, 563))
        screen.blit(checkMark, checkMarkRect)
        checkDisplay = font.render("Check!", True, WHITE, BLACK)
        screen.blit(checkDisplay, (190, 50)) 
    #Player Display

    if currentPlayer == 1:
        turn = "White"
    else:
        turn = "Black"

    turnDisplay = font.render(f'Current turn: {turn}', True, WHITE, BLACK)
    screen.blit(turnDisplay, (90, 10))
    # flip() the display to put your work on screen

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60


