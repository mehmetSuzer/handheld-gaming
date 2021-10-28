

from random import randint
from functions import *

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
        
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240

BLOCK_WIDTH = 8
BASE_FPS = 10


class Snake:
    def __init__(self, width, color):
        # Head of the snake is the LAST element in this list
        self.coordinates = [[SCREEN_WIDTH//2, SCREEN_HEIGHT//2]]
        self.length = 1
        self.width = width
        self.color = color
        self.dir = LEFT
        self.alive = True
              
    def move(self):
        for i in range(self.length-1):
            self.coordinates[i][0] = self.coordinates[i+1][0]
            self.coordinates[i][1] = self.coordinates[i+1][1]
            
        if self.dir == UP:
            self.coordinates[-1][1] -= self.width
        elif self.dir == LEFT:
            self.coordinates[-1][0] -= self.width
        elif self.dir == DOWN:
            self.coordinates[-1][1] += self.width
        elif self.dir == RIGHT:
            self.coordinates[-1][0] += self.width
                      
    def turn(self, direction):
        if direction == UP and self.dir != DOWN:
            self.dir = UP
        elif direction == LEFT and self.dir != RIGHT:
            self.dir = LEFT
        elif direction == DOWN and self.dir != UP:
            self.dir = DOWN
        elif direction == RIGHT and self.dir != LEFT:
            self.dir = RIGHT       
            
    def eat(self):
        x = self.coordinates[-1][0]
        y = self.coordinates[-1][1]
        if self.dir == UP:
            y -= self.width
        elif self.dir == LEFT:
            x -= self.width
        elif self.dir == DOWN:
            y += self.width
        elif self.dir == RIGHT:
            x += self.width
            
        self.coordinates.append([x,y])
        self.length += 1
        
    def check_hit(self):
        # Get coordinates of the head
        x = self.coordinates[-1][0]
        y = self.coordinates[-1][1]
        
        # Check if there is a collusion with walls
        if x < self.width or x > SCREEN_WIDTH-2*self.width or y < self.width or y > SCREEN_HEIGHT-2*self.width:
            self.alive = False
            return
        
        # Check if the snake collides with itself
        for i in range(self.length-1):
            if self.coordinates[i] == [x,y]:
                self.alive = False
                return        
            
    def draw(self, LCD):
        for i in self.coordinates:
            LCD.rect(i[0], i[1], self.width, self.width, self.color)
          
          
class Food:
    def __init__(self, width, color):
        self.width = width
        self.x = randint(1, SCREEN_WIDTH//self.width-2)*self.width
        self.y = randint(1, SCREEN_HEIGHT//self.width-2)*self.width
        self.color = color
        self.eaten = False
        
    def recreate(self):
        self.x = randint(1, SCREEN_WIDTH//self.width-2)*self.width
        self.y = randint(1, SCREEN_HEIGHT//self.width-2)*self.width
        self.eaten = False  
        
    def draw(self, LCD):
        LCD.fill_rect(self.x, self.y, self.width, self.width, self.color)


def redraw_screen(snake, food, LCD):
    LCD.fill(LCD.black)
    
    # Draw walls
    wallColor = LCD.cyan
    for i in range(SCREEN_HEIGHT//BLOCK_WIDTH):
        LCD.fill_rect(0, i*BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH, wallColor)
        LCD.fill_rect(SCREEN_WIDTH-BLOCK_WIDTH, i*BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH, wallColor)
    for i in range(SCREEN_WIDTH//BLOCK_WIDTH):
        LCD.fill_rect(i*BLOCK_WIDTH, 0, BLOCK_WIDTH, BLOCK_WIDTH, wallColor)
        LCD.fill_rect(i*BLOCK_WIDTH, SCREEN_WIDTH-BLOCK_WIDTH, BLOCK_WIDTH, BLOCK_WIDTH, wallColor)              
    
    snake.draw(LCD)
    food.draw(LCD)
    LCD.show()
   
   
def game(LCD):
    snake = Snake(BLOCK_WIDTH, LCD.white)
    food = Food(BLOCK_WIDTH, LCD.red)
    score = 0
    
    LCD.fill(LCD.black)
    LCD.text("SNAKE", 95, 110, LCD.white)
    LCD.show()
    utime.sleep(2)
    
    # Game loop
    while True:
        # Game ends
        if not snake.alive:
            game_over_message(score, LCD)
            return True
        
        # Play-Pause
        if keyB.value() == 0:
            pause_message(LCD)
            
        # Exit Game
        if keyX.value() == 0:
            if exit_game(LCD):
                return False
        
        if food.eaten:
            food.recreate()
        
        if(up.value() == 0):
            snake.turn(UP)
        elif(left.value() == 0):
            snake.turn(LEFT)
        elif(down.value() == 0):
            snake.turn(DOWN)
        elif(right.value() == 0):
            snake.turn(RIGHT)

        xHead = snake.coordinates[-1][0]
        yHead = snake.coordinates[-1][1]
        if (snake.dir == UP and food.x == xHead and food.y == yHead-BLOCK_WIDTH) or (snake.dir == LEFT and food.x == xHead-BLOCK_WIDTH and food.y == yHead) or (snake.dir == DOWN and food.x == xHead and food.y == yHead+BLOCK_WIDTH) or (snake.dir == RIGHT and food.x == xHead+BLOCK_WIDTH and food.y == yHead):
            snake.eat()
            food.eaten = True
            score += 1
        else:
            snake.move()
            snake.check_hit()
    
        redraw_screen(snake, food, LCD)
        utime.sleep(1/(BASE_FPS+score//6))
    
 
 
 
    
    