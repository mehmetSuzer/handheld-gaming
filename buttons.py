
from machine import Pin

up = Pin(2,Pin.IN,Pin.PULL_UP)
down = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
    
keyA = Pin(15,Pin.IN,Pin.PULL_UP) # restart button
keyB = Pin(17,Pin.IN,Pin.PULL_UP) # play-pause button
keyX = Pin(19,Pin.IN,Pin.PULL_UP) # exit button
keyY= Pin(21,Pin.IN,Pin.PULL_UP) # dont exit button







