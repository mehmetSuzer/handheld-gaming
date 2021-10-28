

from random import randint
from functions import *

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
        
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240

FLAPPY_BIRD_FPS = 18

    
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.y_velocity = 0
        self.image = [[0xd56d, 0xd56d, 0xd56d, 0xd56d, 0xd56d, 0xd56d, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0xd56d, 0xd56d, 0xd56d, 0xd56d, 0xd56d],
                      [0xd56d, 0xd56d, 0xd56d, 0xd56d, 0x0000, 0x0000, 0x61ff, 0x61ff, 0x61ff, 0x0000, 0xffff, 0xffff, 0x0000, 0xd56d, 0xd56d, 0xd56d, 0xd56d],
                      [0xd56d, 0xd56d, 0xd56d, 0x0000, 0x61ff, 0x61ff, 0x61ff, 0x61ff, 0x0000, 0xffff, 0xffff, 0xffff, 0xffff, 0x0000, 0xd56d, 0xd56d, 0xd56d],
                      [0xd56d, 0x0000, 0x0000, 0x0000, 0x0000, 0x61ff, 0x61ff, 0x61ff, 0x0000, 0xffff, 0xffff, 0xffff, 0x0000, 0xffff, 0x0000, 0xd56d, 0xd56d],
                      [0x0000, 0x69b5, 0x69b5, 0x69b5, 0x69b5, 0x0000, 0x61ff, 0x61ff, 0x0000, 0xffff, 0xffff, 0xffff, 0x0000, 0xffff, 0x0000, 0xd56d, 0xd56d],
                      [0x0000, 0x69b5, 0x69b5, 0x69b5, 0x69b5, 0x69b5, 0x0000, 0x61ff, 0x61ff, 0x0000, 0xffff, 0xffff, 0xffff, 0xffff, 0x0000, 0xd56d, 0xd56d],
                      [0x0000, 0xd32b, 0x69b5, 0x69b5, 0x69b5, 0xd32b, 0x0000, 0x61ff, 0x61ff, 0x61ff, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0xd56d],
                      [0xd56d, 0x0000, 0xd32b, 0xd32b, 0xd32b, 0x0000, 0x61ff, 0x61ff, 0x61ff, 0x0000, 0x21db, 0x21db, 0x21db, 0x21db, 0x21db, 0x21db, 0x0000],
                      [0xd56d, 0xd56d, 0x0000, 0x0000, 0x0000, 0x0473, 0x0473, 0x0473, 0x0000, 0x21db, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0xd56d],
                      [0xd56d, 0xd56d, 0x0000, 0x0473, 0x0473, 0x0473, 0x0473, 0x0473, 0x0473, 0x0000, 0x21db, 0x21db, 0x21db, 0x21db, 0x21db, 0x0000, 0xd56d],
                      [0xd56d, 0xd56d, 0xd56d, 0x0000, 0x0000, 0x0473, 0x0473, 0x0473, 0x0473, 0x0473, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0xd56d, 0xd56d],
                      [0xd56d, 0xd56d, 0xd56d, 0xd56d, 0xd56d, 0x0000, 0x0000, 0x0000, 0x0000, 0x0000, 0xd56d, 0xd56d, 0xd56d, 0xd56d, 0xd56d, 0xd56d, 0xd56d]]
        self.image_width = len(self.image[0])
        self.image_height = len(self.image)
        self.alive = True
  
    def move(self):
        self.y_velocity += 2
        self.y += self.y_velocity
        
    def draw(self, LCD):
        for row in range(self.image_height):
            for col in range(self.image_width):
                LCD.pixel(self.x+col, self.y+row, self.image[row][col])
                
    def check_hit(self, columns):
        for column in columns:
            if (column.x <= self.x < column.x+column.gap_width or column.x <= self.x+self.image_width < column.x+column.gap_width) and (self.y < column.gap_y or self.y+self.image_height > column.gap_y+column.gap_height):
                self.alive = False
                return
        if not (0 <= self.y+self.image_height < SCREEN_HEIGHT):
            self.alive = False
        
            
class Column:
    def __init__(self, x, gap_y, gap_width, gap_height, color):
        self.x = x
        self.gap_y = gap_y
        self.gap_width = gap_width
        self.gap_height = gap_height
        self.color = color
        self.x_velocity = 4
        self.visible = True # If it is not visible anymore, delete the instance
        self.passed = False # If the bird passes a column, increment the score by one
        
    def move(self):
        self.x -= self.x_velocity
        
    def draw(self, LCD):
        LCD.fill_rect(self.x, 0, self.gap_width, self.gap_y, self.color)
        LCD.fill_rect(self.x, self.gap_y+self.gap_height, self.gap_width, SCREEN_HEIGHT-self.gap_y+self.gap_height, self.color)
        LCD.rect(self.x, 0, self.gap_width, self.gap_y, LCD.black)
        LCD.rect(self.x, self.gap_y+self.gap_height, self.gap_width, SCREEN_HEIGHT-self.gap_y+self.gap_height, LCD.black)       
        LCD.rect(self.x, self.gap_y-20, self.gap_width, 20, LCD.black)
        LCD.rect(self.x, self.gap_y+self.gap_height, self.gap_width, 20, LCD.black)
        
    def check_visibility(self):
        if self.x+self.gap_width < 0:
            self.visible = False


def flappy_bird_redraw_screen(bird, columns, LCD):
    backgroundColor = 0xd56d
    LCD.fill(backgroundColor)
    
    for column in columns:
        column.draw(LCD)
        
    bird.draw(LCD)
    LCD.show()
    
        
def game(LCD):
    bird = Bird(100, 100)
    columns = []
    score = 0
    keyA_is_pressed = False
    column_spawn_count = 0
    
    LCD.fill(LCD.black)
    LCD.text("FLAPPY BIRD", 70, 110, LCD.white)
    LCD.show()
    utime.sleep(2)
    
    # Game loop
    while True:
        # Game Over
        if not bird.alive:
            game_over_message(score, LCD)
            return True
        
        # Play-Pause
        if keyB.value() == 0:
            pause_message(LCD)
            
        # Exit Game
        if keyX.value() == 0:
            if exit_game(LCD):
                return False
            
        if keyA.value() == 0:
            keyA_is_pressed = True
        elif keyA.value() == 1 and keyA_is_pressed:
            bird.y_velocity = -11
            keyA_is_pressed = False
            
        bird.move()
        for column in columns:
            column.move()
        bird.check_hit(columns)
        
        column_spawn_count += 1
        if column_spawn_count == int(2*FLAPPY_BIRD_FPS):
            new_column = Column(240, randint(30, 160), 25, 50, LCD.green)
            columns.append(new_column)
            column_spawn_count = 0
            
        if len(columns) != 0:
            columns[0].check_visibility()
            if not columns[0].visible:
                columns.pop(0)
    
        for column in columns:
            if not column.passed and bird.x > column.x+column.gap_width:
                column.passed = True
                score += 1
                break
                 
        flappy_bird_redraw_screen(bird, columns, LCD)
        utime.sleep(1/FLAPPY_BIRD_FPS)
        

        
        
    
        
        
        
        