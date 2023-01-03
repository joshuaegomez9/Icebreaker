"""
Project Icebreaker v1.23 - Milestone 3

This program will set up a board and create and play an IceBreaker game for 
two players. It will also display status of the game, and coordinates of mouse clicks.

author: Joshua Gomez

"""

# IMPORTS

from graphics import *
import random

#===============================================================================
# GLOBAL CONSTANTS AND VARIABLES

# window title
WIN_TITLE = "Joshua Gomez' Project IceBreaker v1.23 MS3, December 05, 2021"

# number of rows and columns of squares on the gameboard
ROW, COLUMN = 7, 10

# window width and height
WIN_W, WIN_H = 455, 400

# window size
WIN_SIZE = 40

# seperating gaps
GAP = 5

# Ice list (to use for drawing squares and ice)
ices = []

# Dot Images
red_dot = Image(Point(25, 160), "red_dot.gif")
blue_dot = Image(Point(430, 160), "blue_dot.gif")

# Player Turn
player = 0

# Player Position
players = [ [ROW // 2, 0  , red_dot, "PLAYER 0"],
            [ROW // 2, 9  , blue_dot, "PLAYER 1"]] 

# Move or Break Ice
move = True

# Splash Window - Initial Screen
splash_win = GraphWin(WIN_TITLE, WIN_W, WIN_H)

# Used for determining if the user clicked the exit button
exited = False
#===============================================================================

# Initial State
def splash_screen():
    """
    purpose: This function will present a “Splash” screen when game starts 
             showing title, name, and some additional information.
    parameters: None
    return: title, name, instructions, snow
    
    """
    splash_win.setBackground("cyan")
    
    # Title of the game:
    title = Text(Point(228, 35), "☃   IceBreaker Game   ☃") # snowman text
    title.setSize(24)
    title.setStyle("bold")
    title.setFill("dark blue")
    title.draw(splash_win)
    
    # My name 
    name = Text(Point (228, 65), "By: Joshua Gomez")
    name.setSize(16)
    name.setFill("dark blue")
    name.draw(splash_win)
    
    # Brief instructions of the Icebreaker game
    instructions = Text(Point(228, 170), "A fun and simple game for two players!\n\n Move and break ice. \nThe first player unable to move \nloses the game.")
    instructions.setSize(18)
    instructions.setFill("dark blue")
    instructions.draw(splash_win)
    
    # Snow text symbols to make it look pretty
    snow = Text(Point(179,350), "❄       " * 7)
    snow.setFill("dark blue")
    snow.draw(splash_win)
    snow.setSize(30)
    
    return title, name, instructions, snow


def splash_btn(splash_win, x, y, w, h, txt):
    """
    purpose: This function will create rectangle buttons used for the play button in 
             splash_screen, as well as the restart and exit buttons in end_screen
    parameters: splash_win, (x,y,w,h) rectangle measurements, (txt) 'text' for the button
    return: rect (rectangle button/ice), text
    
    """ 
    # Create rectangle buttons with text
    rect = Rectangle(Point(x,y), Point(x+w,y+h))
    rect.setFill("dark blue")
    rect.setOutline("white")
    rect.setWidth(2)
    text = Text(rect.getCenter(), txt)
    text.setSize(18)
    text.setFill("white")
    rect.draw(splash_win)
    text.draw(splash_win)
                    
    return (rect,  text)


def splash_loop(play, title, name, instructions, snow):
    """
    purpose: This function will use helper functions to display the splash screen
             at the start of the program using a loop and will launch the game when 
             “Play Game” button is clicked.
    parameters: play, title, name, instructions, snow
    return: None
    
    """
    global win, splash_win
    
    # splash loop
    while True:
        splash_pt = splash_win.getMouse()
        if in_button(splash_pt, play): # play button clicked
            splash_win.close()
            win = GraphWin(WIN_TITLE, WIN_W, WIN_H) # open the main game window
            
            break
          
    return None


# BOARD SETUP
def set_board(player_text, move_text):
    """
    purpose: This function will set up the board using the 
             the designated number of rows and columns. This is the initial 
             state of the program.
    parameters: player_text, move_text
    return: None
    
    """  
    # Array of Squares and Seperating Gaps
    for i in range(COLUMN):
        ices.append([])
        for j in range(ROW):
            ices[i].append(None)
            
            # Left and top gaps
            left = GAP + i * (WIN_SIZE + GAP)
            top = GAP + j * (WIN_SIZE + GAP)
            
            # Draw rectangle for squares in 'ice'
            r = Rectangle(Point(left, top), Point(left + WIN_SIZE, top + WIN_SIZE))
            r.draw(win)
            r.setFill("white")
            
            ices[i][j] = [r]        
    
    # Two Players: red dot for player 1 and blue dot for player 2    
    red_dot.draw(win)
    blue_dot.draw(win)
    
    # Display text objects
    player_text.setText(f"Player {player}: [{players[0][0]},{players[0][1]}]")
    move_text.setText("MOVE")

    return None


def random_pos():
    """
    purpose: This function will place the two players (red_dot and blue_dot) to a random
             position, with at least one blank square between them (helper function for Reset).
    parameters: None
    return: random0_x, random0_y, random1_x, random1_y
    
    """
    global players
    
    # RESET TO RANDOM POSITIONING OF THE TWO PLAYERS
    # Player 0
    random0_x = random.randint(0, ROW - 1)
    random0_y = random.randint(0, COLUMN - 1)
    
    # Player 1
    random1_x = random.randint(0, ROW - 1)
    random1_y = random.randint(0,COLUMN - 1)
    
    # Must not be in the same square and must have atleast one square between them
    while (random0_x == random1_x and random0_y == random1_y) or (random0_x - 1 <= random1_x <= random0_x + 1 and random0_y - 1 <= random1_y <= random0_y + 1):
        random1_x = random.randint(0, ROW - 1)
        random1_y = random.randint(0,COLUMN - 1) # generate a new random position
        
    
    # Random Player Position
    players = [ [random0_x, random0_y  , red_dot, "PLAYER 0"],
              [random1_x, random1_y , blue_dot, "PLAYER 1"]]     
    
    return random0_x, random0_y, random1_x, random1_y



def Reset(pt, info, reset, player_text, move_text,column, row):
    """
    purpose: This function will reset the program state to the initial program state and
             place the players to a random position if reset button is clicked, or to
             the initial positions if the restart button is clicked.
    parameters: pt, info, reset, player_text, move_text, column, row
    return: None
    
    """   
    global red_dot, blue_dot, player, players, move
    
    # Undraw the red and blue images to reset their position
    red_dot.undraw()
    blue_dot.undraw()
    
    if in_button(pt, reset):
        
        # Reset to random position of the two players - call random_pos
        random0_x, random0_y, random1_x, random1_y = random_pos()        
        red_dot = Image(ices[random0_y][random0_x][0].getCenter(), "red_dot.gif") # new position (click)
        blue_dot = Image(ices[random1_y][random1_x][0].getCenter(), "blue_dot.gif") # new position (click)
        
    else:  # (restart button clicked)
        
        # Initial Player Position
        players = [ [ROW // 2, 0  , red_dot, "PLAYER 0"],
                    [ROW // 2, 9  , blue_dot, "PLAYER 1"]]       
        
        # Dot Images
        red_dot = Image(Point(25, 160), "red_dot.gif")
        blue_dot = Image(Point(430, 160), "blue_dot.gif")        
    
    # Initial state of program - call set_board
    player = 0
    move = True 
    set_board(player_text, move_text)
    
    
    # Wait for mouse click before returning to top of GUI loop   
    win.getMouse()
    
    return None


def info_msg():
    """
    purpose: This function will display informational text message on the state of
             the game and the coordinates of where the user mouse has been clicked.
    parameters: None
    return: info, player_text, move_text
    
    """
    
    # Display informational text object
    info = Text(Point(150, 380), "Mouse")
    info.setSize(14)
    info.draw(win) 
    
    # Display Player text message
    player_text = Text(Point(150, 335), f"Player {player}: [{players[0][0]},{players[0][1]}]")
    player_text.setSize(14)
    player_text.draw(win)
    
    # Display "move" message
    move_text = Text(Point(150, 355), "MOVE")    
    move_text.setSize(14)
    move_text.draw(win)    
    
    return info, player_text, move_text


def btn_create(win, x, y, w, h, txt):
    """
    purpose: This function will create rectangle buttons used for quit and reset
             and the ice squares.
    parameters: win (window), (x,y,w,h) rectangle measurements, (txt) 'text' for the button
    return: rect (rectangle button/ice), text
    
    """ 
    # Create rectangle buttons with text
    rect = Rectangle(Point(x,y), Point(x+w,y+h))
    text = Text(rect.getCenter(), txt)
    text.setSize(12)
    rect.draw(win)
    text.draw(win)
                    
    return (rect,  text)



def in_button(pt, button):
    """
    purpose: This function will determine if a user mouse click is inside a 
             button or square.
    parameters: pt (mouse click point), button
    return: Boolean (True/False) variables depending on whether a click is inside a button/square
    
    """
    # If mouse click coordinates are in between (inside) button rectangles coordinates, return True
    if button[0].getP1().x < pt.x < button[0].getP2().x and button[0].getP1().y < pt.y < button[0].getP2().y:
        return True
    
    return False # Otherwise, return False
  
    
def player_turn(player_text):
    """
    purpose: This function will determine and return whose turn it is (player 0 or player 1) and
             display the player coordinates  (helper function for square_click)
    parameters: player_text
    return: player
    """
    global player
    
    # Alternate between 0 and 1
    player = (player + 1) % 2
    
    if player == 0: # Player 0 - display coords
        player_text.setText(f"Player {player}: [{players[0][0]},{players[0][1]}]")
        
    else: # Player 1 - display coords
        player_text.setText(f"Player {player}: [{players[1][0]},{players[1][1]}]") 
        
    return player    


def valid_move(pt, column, row):
    """
    purpose: This function will detect and report a boolean value depending on whether
             the player made a legal, valid move (adjacent square, unbroken ice, unoccupied by opponent)
               (helper function for square_click)
    patameters: pt, column, row
    return: Boolean (True/False) variables depending on whether a move is valid
    """
    global players
    
    # Square coordinates of the click
    click_coord = (row, column)
    
    # Player 0
    if player == 0:
        
        # Adjacent squares - click must be between -1, and +1 of the player position
        if players[0][0] - 1 <= click_coord[0] <= players[0][0] + 1 and players[0][1] - 1 <= click_coord[1] <= players[0][1] + 1:
            
            # Square must be unbroken ice and unoccupied to be a valid square
            if ices[column][row][0].config['fill'] != 'cyan' and click_coord != (players[0][0], players[0][1]) and click_coord != (players[1][0], players[1][1]): 
                players[0][0] = row
                players[0][1] = column # new player positions
                return True
    
    # Player 1
    elif player == 1:
        
        # Adjacent squares - click must be between -1, and 1 of the player position
        if players[1][0] - 1 <= click_coord[0] <= players[1][0] + 1 and players[1][1] - 1 <= click_coord[1] <= players[1][1] + 1:
            
            # Squares must be unbroken ice and unoccupied to be a valid square
            if ices[column][row][0].config['fill'] != 'cyan' and click_coord != (players[1][0], players[1][1]) and click_coord != (players[0][0], players[0][1]):
                players[1][0] = row
                players[1][1] = column # new player positions
                return True
        
    return False
 
 
def move_players(column, row):
    """
    purpose: This function will help move the red_dot and blue_dot images (players) according to
             the valid move clicked  (helper function for square_click)
    parameter: column, row
    return: None
    """
    global red_dot, blue_dot
    
    # Player 0
    if player == 0:
        red_dot.undraw()
        red_dot = Image(ices[column][row][0].getCenter(), "red_dot.gif") # new position (click)
        red_dot.draw(win)
      
    # Player 1  
    else:
        blue_dot.undraw()
        blue_dot = Image(ices[column][row][0].getCenter(), "blue_dot.gif") # new position (click)
        blue_dot.draw(win)
        
        return None
    

def square_click(pt, column, row, info, player_text, move_text):
    """
    purpose: This function will call other helper functions to excecute the actions
             when a player clicks a square. It will either move the player to a valid square,
             break the ice, or indicate that there is an invalid move. 
    parameters: pt, column, row, info, player_text, move_text
    return: None
    """
    global move, player
    
    # Square coordinates of the click
    click_coord = (row, column)    
    
    # Move - player clicks on legitimate squares
    if move == True:
        if valid_move(pt, column, row): # legal, valid move (adjacent, unbroken ice, unoccupied)
            move_players(column, row)
            player_text.setText(f"Player {player}")
            move_text.setText("BREAK ICE")
            move = False # move is over when player successfully moves on a square - break ice next
            
        else: # not legal, valid square
            info.setText("NOT VALID")
            
    # When move is over, break the ice      
    elif move == False:
        if ices[column][row][0].config['fill'] != 'cyan' and click_coord != (players[1][0], players[1][1]) and click_coord != (players[0][0], players[0][1]):
            ices[column][row][0].setFill("cyan")
            move_text.setText("MOVE")
            move = True   # once ice is broken, next player makes move
            player = player_turn(player_text) # player turn
        else:
            info.setText("NOT VALID")
       
        
    return None


def has_legal_move():
    """
    purpose: This program will determine if a player has a legal (unbroken, unoccupied)
             square to move to. If there is a possible legal move, return True. (helper function for show_winners)
    paraneters: None
    return: True/False - depending on whether there is a legal square to move to.
            
    """

    global player, players, ROW, COLUMN
    
    # Adjacent squares
    adj = ( (-1, -1), (-1, 0), (-1, 1),    # One row above
    
               ( 0, -1),      ( 0, 1),    # Same row
    
               ( 1, -1), ( 1, 0), ( 1, 1) )   # One row below
    
    # Current player row and column
    player_row, player_col = players[player][:2]          
    
    
    for dr, dc in adj:
        adj_row, adj_col = player_row + dr , player_col + dc      # row, col of each adjacent square
        
        # Row and column of adjacent square must be on board, not other player, and unbroken (white):
        if 0 <= adj_row < ROW and 0 <= adj_col < COLUMN and [adj_row, adj_col] != players[1-player][:2] \
           and ices[adj_col][adj_row][0].config['fill'] == 'white':
               
            return True
        
    return False      
    
def show_winners(pt, info, move, player_text, move_text, column, row, reset):
    """
    purpose: This function will announce the winners (detects if a player
             can't move)
    parameters: pt, info, move, player_text, move_text, column, row, reset
    return: None
    
    """
    global player, exited
    
    # Game ends if a player is unable to move (no more legal moves)
    if has_legal_move() == False: 
        if player == 0:
            info.setText("")
            player = 1                          # other player wins
            player_text.setText("PLAYER 1")
            move_text.setText("WINNER: PLAYER 1")
            end_loop(pt, info, player_text, move_text,column, row, reset) # show end screen
            
        elif player == 1:
            info.setText("")
            player = 0                          # other player wins
            player_text.setText("PLAYER 0")
            move_text.setText("WINNER: PLAYER 0")
            end_loop(pt, info, player_text, move_text,column, row, reset) # show end screen
        
    return None
                     
def end_loop(pt, info, player_text, move_text,column, row, reset):
    """
    purpose: This function is the helper loop for when the game has ended.
             It will call helper functions to display the end screen and
             prompt user to terminate game and exit, or to restart.
    parameters: pt, info, player_text, move_text, column, row, reset
    return: None
    
    """
    global exited
    
    # Seperate end window
    end_win = GraphWin(WIN_TITLE, WIN_W, WIN_H)
    end_win.setBackground("black")
    
    # State the winner
    winner =  Text(Point(228, 75), f"PLAYER {player} WINS!")
    winner.setSize(26)
    winner.setStyle("bold")
    winner.setFill("white")
    winner.draw(end_win)
    
    # Create restart button
    restart = splash_btn(end_win, 145, 150, 165, 40, "RESTART")   
    
    # Create exit button
    exit = splash_btn(end_win, 145, 210, 165, 40, "EXIT")     
    
    while True:
        end_pt = end_win.getMouse()
        
        # restart button clicked
        if in_button(end_pt, restart):
            end_win.close()
            info.setText("RESTART")
            Reset(pt, info, reset, player_text, move_text,column, row)
            break
        
        # exit button clicked    
        elif in_button(end_pt, exit):
            end_win.close()
            exited = True
            break
        
    return None

    
# Helper Function - main gui loop
def main_gui_loop(info, move_text, player_text, play, quit, reset):
    """
    purpose: This helper function is the main gui loop to use the program
    parameters: info (text object), move_text, player_text, play, quit, reset
    return: None
    
    """   
    global win, player, move, state, exited
    

    while True: #---------------------------------------------- MAIN UI LOOP
          
        pt = win.getMouse()

        # x and y squares in columns and rows
        column = int((pt.x - GAP) / (WIN_SIZE + GAP))
        row = int((pt.y - GAP) / (WIN_SIZE + GAP))
        
        # quit button clicked                 
        if in_button(pt, quit):
            info.setText("BYE BYE")
            break        
        
        # reset button clicked
        elif in_button(pt, reset): 
            info.setText("RESET")
            Reset(pt, info, reset, player_text, move_text,column, row)
         
        # squares clicked 
        elif pt.y < 315 and in_button(pt, ices[column][row]):
            info.setText("(" + str(row) + ", " + str(column) + ")")
            square_click(pt, column, row, info, player_text, move_text)
            
            
        # clicked elsewhere - display coordinates
        else:
            info.setText("mouse click (" + str(int(pt.getX())) + ", " + str(int(pt.getY())) + ")") 
                  
        
        show_winners(pt, info, move, player_text, move_text, column, row, reset)  # winners
        
        if exited == True:  # exit button clicked
            win.close()
            return None
            

    win.getMouse()                          # pause before exit
    win.close()
    return None

    
# Main Function
def main():
    """
    purpose: This function is the main function of the program and will call
             helper functions to make the icebreaker game.
    parameters: None
    return: None
    
    """
    
    # SPLASH SCREEN
    title, name, instructions, snow = splash_screen()
    
    # Create play button
    play = splash_btn(splash_win, 145, 270, 165, 40, "PLAY GAME")
    
    # SPLASH SCREEN
    splash_loop(play, title, name, instructions, snow)
    
    # ICEBREAKER GAME
    # Set up board and display informational text message
    info, player_text, move_text = info_msg()
    set_board(player_text, move_text)
    
    # Create quit button
    quit = btn_create(win, 350, 330, 55, 20, "QUIT")
    
    # Create reset button
    reset = btn_create(win, 350, 355, 55, 20, "RESET")  
    
    # Call main loop
    main_gui_loop(info, move_text, player_text, play, quit, reset)
    
    return None
     
#===============================================================================
if __name__ == "__main__":
    main() 