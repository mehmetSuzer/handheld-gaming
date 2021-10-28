

from buttons import *
import utime


def turn_back_to_game_message(LCD):
    count = 3
    while count > 0:
        LCD.fill(LCD.black)
        LCD.text("GAME BEGINS", 70, 80, LCD.white)
        LCD.text("IN {} SECONDS".format(count), 65, 100, LCD.white)
        LCD.show()
        utime.sleep(1)
        count -= 1
        

def pause_message(LCD):
    utime.sleep(0.5)
    count = 1
    while keyB.value() == 1:
        LCD.fill(LCD.black)
        LCD.text("PAUSED", 90, 80, LCD.white)
        if (count%12) % 6 != 0:
            LCD.text("PRESS B TO CONTINUE", 40, 110, LCD.cyan) # This text blinks
        LCD.show()
        utime.sleep(0.08)
        count += 1
    turn_back_to_game_message(LCD)
            
            
def game_over_message(score, LCD):
    utime.sleep(0.5)
    count = 1
    while keyA.value() == 1:
        LCD.fill(LCD.black)
        LCD.text("SCORE: {}".format(score), 80, 80, LCD.white)
        if (count%12) % 6 != 0:
            LCD.text("PRESS A TO RESTART", 50, 110, LCD.cyan) # This text blinks
        LCD.show()
        utime.sleep(0.08)
        count += 1
        
        
def tictactoe_game_end(winner, LCD):
    utime.sleep(0.5)
    count = 1
    while keyA.value() == 1:
        LCD.fill(LCD.black)
        if winner is not None:
            LCD.text("{} PLAYER WON".format(winner), 65, 80, LCD.white)
        else:
            LCD.text("IT'S A DRAW", 70, 80, LCD.white)
        if (count%12) % 6 != 0:
            LCD.text("PRESS A TO RESTART", 50, 110, LCD.cyan) # This text blinks
        LCD.show()
        utime.sleep(0.08)
        count += 1
        
        
def tictactoe_starting_message(LCD):
    count = 0
    while keyA.value() == 1:
        LCD.fill(LCD.black)
        LCD.text("BEFORE STARTING THE GAME", 23, 60, LCD.white)
        LCD.text("CHOOSE X PLAYER AND O PLAYER", 7, 80, LCD.white)
        if (count%12) % 6 != 0:
            LCD.text("PRESS A TO START", 55, 130, LCD.cyan) # This text blinks
        LCD.show()
        utime.sleep(0.08)
        count += 1
    utime.sleep(0.2)

        
def exit_game(LCD):
    utime.sleep(0.5)
    yes_selected = True
    while True:
        LCD.fill(LCD.black)
        LCD.text("DO YOU REALLY", 70, 80, LCD.white)
        LCD.text("WANT TO EXIT?", 70, 100, LCD.white)
        LCD.text("PRESS X TO CHOOSE", 55, 130, LCD.cyan)

        if yes_selected:
            LCD.fill_rect(35, 174, 34, 20, LCD.cyan)
            LCD.text("YES", 40, 180, LCD.black) 
            LCD.text("NO", 185, 180, LCD.cyan)
        else:
            LCD.fill_rect(180, 174, 26, 20, LCD.cyan)
            LCD.text("YES", 40, 180, LCD.cyan) 
            LCD.text("NO", 185, 180, LCD.black)   
        LCD.show()
        utime.sleep(0.12)
        
        if left.value() == 0 or right.value() == 0:
            yes_selected = not yes_selected
            
        if keyX.value() == 0:
            if yes_selected:
                return True
            else:
                turn_back_to_game_message(LCD)
                return False
        
        
        
        
        
        
        