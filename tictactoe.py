

from random import choice
from functions import *

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
        
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240


class Table:
    def __init__(self):
        self.matrix = [[" ", " ", " "],
                       [" ", " ", " "],
                       [" ", " ", " "]]
        
    def draw(self, LCD):
        LCD.fill_rect(85, 25, 5, 190, LCD.white)
        LCD.fill_rect(150, 25, 5, 190, LCD.white)
        LCD.fill_rect(25, 85, 190, 5, LCD.white)
        LCD.fill_rect(25, 150, 190, 5, LCD.white)


class Player:
    def __init__(self, symbol, color):
        self.symbol = symbol
        self.color = color
        self.row = 0
        self.col = 0
        
    def move(self, direction):
        if direction == UP:
            self.row = (self.row-1)%3
        elif direction == LEFT:
            self.col = (self.col-1)%3
        elif direction == DOWN:
            self.row = (self.row+1)%3
        elif direction == RIGHT:
            self.col = (self.col+1)%3
            
    def put_symbol(self, table):
        if table.matrix[self.row][self.col] == " ":
            table.matrix[self.row][self.col] = self.symbol
            return True
        return False
            
    def draw(self, LCD):
        LCD.fill_rect(20+65*self.col, 20+65*self.row, 70, 70, self.color)
        LCD.fill_rect(25+65*self.col, 25+65*self.row, 60, 60, LCD.black)
        

def draw_X(row, col, LCD):
    x = 65*col + 37
    y = 65*row + 34
    for i in range(4):
        LCD.line(x-i, y+i, x-i+40, y+i+40, LCD.white)
    x = 65*col + 73
    y = 65*row + 33
    for i in range(4):
        LCD.line(x+i, y+i, x+i-40, y+i+40, LCD.white)   


def draw_O(row, col, LCD):
    x = 65*col + 35
    y = 65*row + 35
    for i in range(20):
        for j in range(20):
            if 64 <= (i-10)**2 + (j-10)**2 < 100:
                LCD.fill_rect(x+2*i, y+2*j, 2, 2, LCD.white)
            
            
def redraw_screen(curr_player, table, LCD):
    LCD.fill(LCD.black)
    LCD.text("{} PLAYER'S TURN".format(curr_player.symbol), 65, 5, curr_player.color)
    table.draw(LCD)
    curr_player.draw(LCD)
            
    for row in range(3):
        for col in range(3):
            if table.matrix[row][col] == "X":
                draw_X(row, col, LCD)
            elif table.matrix[row][col] == "O":
                draw_O(row, col, LCD)
    LCD.show()
    
    
def win(table):
    for row in table:
        if row.count("X") == 3 or row.count("O") == 3:
            return True
        
    for i in range(3):
        col = [table[0][i], table[1][i], table[2][i]]
        if col.count("X") == 3 or col.count("O") == 3:
            return True
        
    diagonal1 = [table[i][i] for i in range(3)]
    diagonal2 = [table[2-i][i] for i in range(3)]
    if diagonal1.count("X") == 3 or diagonal1.count("O") == 3 or  diagonal2.count("X") == 3 or diagonal2.count("O") == 3:
        return True
    
    return False
  
            
def game(LCD):
    LCD.fill(LCD.black)
    LCD.text("TIC-TAC-TOE", 75, 110, LCD.white)
    LCD.show()
    utime.sleep(2)
    
    tictactoe_starting_message(LCD)
    
    player1 = Player("X", LCD.cyan)
    player2 = Player("O", LCD.yellow)
    current_player = choice([player1, player2])
    table = Table()
    count = 0
            
    # Game loop
    while count != 9 and not win(table.matrix):
        # Play-Pause
        if keyB.value() == 0:
            pause_message(LCD)
            
        # Exit Game
        if keyX.value() == 0:
            if exit_game(LCD):
                return False
            
        if up.value() == 0:
            current_player.move(UP)
        elif left.value() == 0:
            current_player.move(LEFT)
        elif down.value() == 0:
            current_player.move(DOWN)
        elif right.value() == 0:
            current_player.move(RIGHT)
            
        if keyA.value() == 0 and current_player.put_symbol(table):
            if current_player == player1:
                current_player = player2
            else:
                current_player = player1
            count += 1
            utime.sleep(0.2)
            
        redraw_screen(current_player, table, LCD)
        utime.sleep(0.1 - count**2 / 1000) # The amount of delay is reduced to compensate the increasing time required to draw the table
        
    utime.sleep(0.7)
    winner = None
    if win(table.matrix):
        if current_player == player1:
            winner = "O"
        else:
            winner = "X"
            
    tictactoe_game_end(winner, LCD)
    return True
            
        
            
            
  
            
        