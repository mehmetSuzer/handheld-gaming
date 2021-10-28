

from machine import Pin,SPI,PWM
from random import randint
import utime

from buttons import *
import flappy_bird
import snake
import spaceship
import tictactoe
import lcd

        
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
        
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240

LOOP_FREQ = 16 # Pick an even number

def turn_off():
    utime.sleep(0.5)
    yes_selected = True
    while True:
        LCD.fill(LCD.black)
        LCD.text("DO YOU REALLY WANT TO", 35, 80, LCD.white)
        LCD.text("TURN OFF THE DEVICE?", 40, 100, LCD.white)
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
                LCD.fill(LCD.black)
                LCD.text("GOOD BYE", 85, 80, LCD.cyan)
                LCD.show()
                utime.sleep(2)
                LCD.fill(LCD.black)
                LCD.show()
                return True
            else:
                utime.sleep(0.3) # Wait a little bit to avoid a accidental press
                return False


if __name__ == "__main__":
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)

    LCD = lcd.LCD_1inch3(SCREEN_WIDTH, SCREEN_HEIGHT)
    LCD.fill(LCD.black)
    LCD.show()
    
    # Names of games should contain max 22 characters
    games = ["SNAKE", "SPACESHIP", "FLAPPY BIRD", "TIC-TAC-TOE(2 PLAYERS)"]
    index = 0
    count = 1

    # Main loop
    while True:
        LCD.fill(LCD.black)
        if (count%LOOP_FREQ) % (LOOP_FREQ//2) != 0:
            LCD.text("PRESS X TO PLAY GAME", 40, 25, LCD.cyan) # This text blinks
        for i in range(len(games)):
            if i == index:
                LCD.fill_rect(15, 56+i*15, 10, 3, LCD.white)
                LCD.fill_rect(30, 50+i*15, 180, 15, LCD.white)
                LCD.text(games[i], 35, 54+i*15, LCD.black)
            else:
                LCD.text(games[i], 35, 54+i*15, LCD.white)
        LCD.show()
        utime.sleep(1/LOOP_FREQ)
        count += 1
        
        if keyX.value() == 0:
            if games[index] == "SNAKE":
                while snake.game(LCD): # The function returns False if the user exits the game
                    pass
            elif games[index] == "SPACESHIP":
                while spaceship.game(LCD): # The function returns False if the user exits the game
                    pass
            elif games[index] == "FLAPPY BIRD":
                while flappy_bird.game(LCD): # The function returns False if the user exits the game
                    pass
            elif games[index] == "TIC-TAC-TOE(2 PLAYERS)":
                while tictactoe.game(LCD): # The function returns False if the user exits the game
                    pass
                
            utime.sleep(0.3) # Wait a little to avoid restarting the same game
            count = 1
            
        if keyY.value() == 0 and turn_off(): # Safely turn off the device
            break     
                
        if count % 2 == 0: # 2*LOOP_FREQ seconds sleep for the joystick
            if up.value() == 0:
                index = (index-1) % len(games)
            elif down.value() == 0:
                index = (index+1) % len(games)
            
            
        
        
        
        
        
        
        
        
        
        