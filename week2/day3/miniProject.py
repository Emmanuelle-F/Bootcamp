# initialise board
def initialiseBoard():
    return [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]

# Display the Game Board
def displayBoard(board):
    for i, row in enumerate(board):
        print(f"   {row[0]} | {row[1]} | {row[2]}")
        if i < 2:
            print("  ---+---+---")


# Register the players
def registerPlayer():
    print ("\n")
    player1Name = input ("Player 1, please enter your name: ")
    player2Name= input ("Player 2, please enter your name: ")

    player1 = {"name" : player1Name, "symbol" : "O"}
    player2 = {"name" : player2Name, "symbol" : "X"}

    print ("\n")
    print (f"Player 1 : {player1Name} \nPlayer 2: {player2Name}")

    return [player1, player2]


# Getting Player Input  
def playerInput(board, player):

    validPosition = False
    rowPosition = 0
    columnPosition =0

    playerName = player["name"]

    while not validPosition: 
        
        print ("\n")
        rowPosition = int(input (f"{playerName} please enter a valid row from 1 to 3: ")) - 1
        columnPosition = int(input (f"{playerName} please enter a valid column from 1 to 3: ")) - 1

        if 0 <= rowPosition <= 2 and 0 <= columnPosition <= 2:
            if board[rowPosition][columnPosition] == ' ':
                validPosition = True
                return rowPosition, columnPosition
            else:
                print ("Cell is already taken")
        else:
            print ("Enter a valid row and column position")

# check for win
def checkWin(board, player):

    symbol = player["symbol"]

    for i in range (0,2):
        # horizontally
        if board[i][0] == symbol and board[i][1] == symbol and board[i][2] == symbol:
            return "win"
        # vertically
        if board[0][i] == symbol and board[1][i] == symbol and board[2][i] == symbol:
            return "win"
        
    # diagonally
    if board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol:
        return "win"
    elif board[2][0] == symbol and board[1][1] == symbol and board[0][2] == symbol:
        return "win"
       

    # # horizontally
    # if board[0][0] == symbol and board[0][1] == symbol and board[0][2] == symbol:
    #     return "win"
    # elif board[1][0] == symbol and board[1][1] == symbol and board[1][2] == symbol:
    #     return "win"
    # elif board[2][0] == symbol and board[2][1] == symbol and board[2][2] == symbol:
    #     return "win"
    # # vertically
    # elif board[0][0] == symbol and board[1][0] == symbol and board[2][0] == symbol:
    #     return "win"
    # elif board[0][1] == symbol and board[1][1] == symbol and board[2][1] == symbol:
    #     return "win"
    # elif board[0][2] == symbol and board[1][2] == symbol and board[2][2] == symbol:
    #     return "win"
    # # diagonally
    # elif board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol:
    #     return "win"
    # elif board[2][0] == symbol and board[1][1] == symbol and board[0][2] == symbol:
    #     return "win"

def checkDraw(board):
    emptyCell = " "
    for row in board:
        if emptyCell in row:
            return ""
    
    return "Draw"
            


# play

def play():
    board = initialiseBoard()

    displayBoard(board)

    players = registerPlayer()

    gameOver = False

    while gameOver == False:
        for player in players:
            rowPosition, columnPosition = playerInput(board, player)

            board[rowPosition][columnPosition] = player["symbol"]

            displayBoard(board)

            # check for win
            resultWin = checkWin(board, player)

            if resultWin == "win":
                gameOver = True
                print (f"{player["name"]} is the winner!")
                break
            else:
                # check for draw
                resultDraw = checkDraw(board)

                if resultDraw == "Draw":
                    gameOver = True
                    print ("It is a draw!")
                    break
            
# Main program
play()