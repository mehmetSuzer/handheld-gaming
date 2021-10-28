

from random import randint
from functions import *

UP = 0
LEFT = 1
DOWN = 2
RIGHT = 3
        
SCREEN_WIDTH = 240
SCREEN_HEIGHT = 240

# Use these variables to adjust the difficulty of the game
SIZE = 3
ASTEROID_SIZE_MULTIPLIER = 6
ASTEROID_SPAWN_PERIOD = 4
MAX_ASTEROID = 15
FPS = 12

        
class Asteroid:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = ASTEROID_SIZE_MULTIPLIER*size
        self.color = color
        self.health = 50
        self.gone = False
        
    def move(self):
        self.y += self.size//3
        
    def draw(self, LCD):
        LCD.fill_rect(self.x, self.y, self.size, self.size, self.color)
        
    def check_borders(self):
        if self.y > SCREEN_HEIGHT:
            self.gone = True
        
class Bullet:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.gone = False
        
    def move(self):
        self.y -= 4*self.size
        
    def check_borders(self):
        if self.y+self.size < 0:
            self.gone = True
            
    def check_asteroid_hit(self, asteroids):
        for asteroid in asteroids:
            if asteroid.x <= self.x < asteroid.x+asteroid.size and asteroid.y <= self.y < asteroid.y+asteroid.size:
                self.gone = True
                asteroid.health -= 10
                if asteroid.health <= 0:
                    asteroid.gone = True
                break
            
    def draw(self, LCD):
        LCD.fill_rect(self.x, self.y, self.size, self.size, self.color)        
        
        
class Spaceship:
    def __init__(self, x, y, size, color):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.dir = None
        self.bullets = []
        self.maxBullet = 12
        self.bulletCount = self.maxBullet
        self.health = 100
        
    def move(self, asteroids):
        if self.dir == LEFT and self.x-5*self.size > 0:
            self.x -= 3*self.size
        elif self.dir == RIGHT and self.x+5*self.size < SCREEN_WIDTH:
            self.x += 3*self.size
        elif self.dir == UP and self.y > 16*self.size:
            self.y -= 3*self.size
        elif self.dir == DOWN and self.y+8*self.size < SCREEN_HEIGHT:
            self.y += 3*self.size
        
        # Move the bullets and check whether they hit an asteroid or go out of the screen
        for bullet in self.bullets:
            bullet.move()
            bullet.check_asteroid_hit(asteroids)
            bullet.check_borders()
        self.check_bullets()
            
    def draw(self, LCD):
        # Draw the spaceship
        for i in range(6):
            LCD.fill_rect(self.x-i*self.size, self.y+i*self.size, self.size*(2*i+1), self.size, self.color)
        LCD.fill_rect(self.x-3*self.size, self.y+6*self.size, int(1.5*self.size), 2*self.size, self.color)
        LCD.fill_rect(self.x+int(2.5*self.size), self.y+6*self.size, int(1.5*self.size), 2*self.size, self.color)
        
        # Draw the exhaust fire
        if self.dir == UP:
            LCD.fill_rect(self.x-3*self.size, self.y+9*self.size, int(1.5*self.size), 4*self.size, LCD.blue)
            LCD.fill_rect(self.x+int(2.5*self.size), self.y+9*self.size, int(1.5*self.size), 4*self.size, LCD.blue)
     
         # Draw bullets
        for bullet in self.bullets:
            bullet.draw(LCD)
          
        # Draw the bullet bar
        LCD.fill_rect(3*SIZE, 3*SIZE, self.bulletCount*SIZE, 2*SIZE, LCD.green)
        LCD.fill_rect((3+self.bulletCount)*SIZE, 3*SIZE, (self.maxBullet-self.bulletCount)*SIZE, 2*SIZE, LCD.red)
        LCD.rect(3*SIZE, 3*SIZE, self.maxBullet*SIZE, 2*SIZE, LCD.white)
        
        # Draw the health bar
        LCD.fill_rect(SCREEN_WIDTH-13*SIZE, 3*SIZE, (self.health//10)*SIZE, 2*SIZE, LCD.green)
        LCD.fill_rect(SCREEN_WIDTH+(self.health//10-13)*SIZE, 3*SIZE, (10-self.health//10)*SIZE, 2*SIZE, LCD.red)
        LCD.rect(SCREEN_WIDTH-13*SIZE, 3*SIZE, 10*SIZE, 2*SIZE, LCD.white)
     
    def fire(self):
        if self.bulletCount > 1:
            bulletColor = 0x001f
            bullet = Bullet(self.x-3*self.size, self.y+2*self.size, self.size, bulletColor)
            self.bullets.append(bullet)
            bullet = Bullet(self.x+3*self.size, self.y+2*self.size, self.size, bulletColor)
            self.bullets.append(bullet)
            self.bulletCount -= 2
            
    def check_bullets(self):
        # Remove bullets that are gone
        newBullets = []
        for bullet in self.bullets:
            if not bullet.gone:
                 newBullets.append(bullet)
        self.bullets = newBullets
        
    def check_asteroid_hit(self, asteroids):
        for asteroid in asteroids:
            if not asteroid.gone:
                for i in range(6):
                    if (asteroid.x <= self.x+i*self.size < asteroid.x+asteroid.size or asteroid.x <= self.x-i*self.size < asteroid.x+asteroid.size) and asteroid.y <= self.y+i*self.size < asteroid.y+asteroid.size:
                        self.health -= 10
                        asteroid.gone = True
                        break
     
     
def redraw_screen(ship, asteroids, LCD):
    LCD.fill(LCD.black)
    for asteroid in asteroids:
        asteroid.draw(LCD)
    ship.draw(LCD)
    LCD.show()

   
def game(LCD):
    ship = Spaceship(120, 120, SIZE, LCD.cyan)
    asteroids = []
    newAsteroids = []
    score = 0
    bulletReloadCount = 0

    LCD.fill(LCD.black)
    LCD.text("SPACESHIP", 80, 110, LCD.white)
    LCD.show()
    utime.sleep(2)
    
    # Game loop
    while True:
        # Game ends
        if ship.health <= 0:
            game_over_message(score, LCD)
            return True
        
        # Play-Pause
        if keyB.value() == 0:
            pause_message(LCD)
            
        # Exit Game
        if keyX.value() == 0:
            if exit_game(LCD):
                return False
            
        # Add new asteroids
        if len(asteroids) < MAX_ASTEROID and randint(0, ASTEROID_SPAWN_PERIOD) == 0:
            asteroid = Asteroid(randint(0, SCREEN_WIDTH-ASTEROID_SIZE_MULTIPLIER*SIZE), -ASTEROID_SIZE_MULTIPLIER*SIZE, SIZE, LCD.yellow)
            asteroids.append(asteroid)
            
        # Increment bulletCount in every step
        if ship.bulletCount < ship.maxBullet:
            bulletReloadCount += 1
            if bulletReloadCount == 2:
                ship.bulletCount += 1
                bulletReloadCount = 0
        
        # Check whether a button is pressed
        if up.value() == 0:
            ship.dir = UP
        elif left.value() == 0:
            ship.dir = LEFT
        elif down.value() == 0:
            ship.dir = DOWN
        elif right.value() == 0:
            ship.dir = RIGHT
        else:
            ship.dir = None
            
        if keyA.value() == 0:
            ship.fire()
            
        # Move the ship and check whether it is hit by an asteroid
        # If an asteroid is destroyed by bullets, increment the score
        ship.move(asteroids)
        for asteroid in asteroids:
            if asteroid.gone:
                score += 1
        ship.check_asteroid_hit(asteroids)
            
        # Move asteroids and update the asteroid list
        for asteroid in asteroids:
            asteroid.move()
            asteroid.check_borders()
            if not asteroid.gone:
                newAsteroids.append(asteroid)
        asteroids = newAsteroids
        newAsteroids = []
        
        # Redraw the window and wait 100 ms
        redraw_screen(ship, asteroids, LCD)
        utime.sleep(1/FPS)
        
        
        
    
        
        
        
        
        