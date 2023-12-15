# this file was created by Nolan Keith

# Game name: "Aestroids Game"
# Sources: Chris Cozort; Chris Bradfield; Alan Kim; Will Goodman; learntocodeGCSE
# Goals: create a aestroids game and understand all components clearly


# Things I could not Achieve

'''
- bullet mechanism
- attempted background switch during game progression
- wanted to add lives but was unable to get to do that
'''


# import libraries for game use
import pygame, time, sys
from pygame.locals import *
import random

pygame.init()



# game frames settings
FPS = 30
framesPerSec = pygame.time.Clock()

# define colors 
black = (0,0,0)
red = (255, 0, 0)


# window display for game -  top left of window
window = pygame.display.set_mode((500,600))
window.fill(black)
pygame.display.set_caption("Aestroid Game")


# define rocket horizontal speed
speed = 10

# setting a width and height for window
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()


# import game music 
from pygame import mixer
mixer.init()
mixer.music.load("space.mp3")
mixer.music.set_volume(0.5)
mixer.music.play()


# enemy class for in game use - aestroids
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # img for enemy entity
        self.image = pygame.image.load("Asteroid.png")
        self.surf = pygame.Surface((30,30))
        self.rect = self.surf.get_rect(center = (random.randint(40,460), (random.randint(-100,0))))

# enemy class speeds up as progress
    def move(self, score, destroyed):
        self.rect.move_ip(0,speed)
        if(self.rect.bottom > 600) or destroyed == True:
            # score increase for each progression 
            self.rect.center = (random.randint(30,460), (random.randint(-100,0)))
            score += 1

        return score

    # position of objects
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# player class - rocket
class Player(pygame.sprite.Sprite):
    def __init__(self):
        # space ship dislayed image and conents (size)
        super().__init__()
        self.image = pygame.image.load("spaceShip.png")
        # size of spaceship
        self.surf = pygame.Surface((54,118))
        self.rect = self.surf.get_rect(midbottom = (SCREEN_WIDTH / 2, SCREEN_HEIGHT))

    # player position throughout game
    def draw(self, surface):
        surface.blit(self.image, (self.rect.centerx-45, self.rect.centery - 90))

    # establish controls 
    def update(self):
        pressedKeys = pygame.key.get_pressed()
        
        # horizontal left
        if self.rect.left > 0:
            if pressedKeys[K_a]:
                self.rect.move_ip(-5, 0)

        # horizontal right
        if self.rect.right < SCREEN_WIDTH:
            if pressedKeys[K_d]:
                self.rect.move_ip(5, 0)


# bullet class for defensive mechanism
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        # bullet appearance and size - instantiation
        super().__init__()
        self.image = pygame.image.load("bullet.png")
        self.surf = pygame.Surface((10,10))
        # rectangular format for bullet - return after collision
        self.rect = self.surf.get_rect(center = (player.rect.midtop))
        self.fired = False

    # create a bullet that has delay to create a enjoyable experience
    def fire(self, player):
        # key bind for bullet firing - space bar
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys [K_SPACE] and self.fired == False:
            # if space pressed a red bullet will shoot to defend ship
            self.rect = self.surf.get_rect(center = (player.rect.midtop))
            self.fired = True

        # image appearance of bullet
        if self.fired == True:
            window.blit(self.image, self.rect)
            self.rect.move_ip(0,-5)

            # movement of bullet across screen 
            if (self.rect.top < 1):
                self.rect.top = 600
                self.fired = False

    # bullet movement
    def resetPos(self):
        self.rect.top = 600
        self.fired = False

# developing a background for game
class Background():
    def __init__(self):
        # space png
        self.backgroundImage = pygame.image.load("backgroundImage2.png")
        self.rectBGimage = self.backgroundImage.get_rect()
        
        # positioning of background images
        self.bgY1 = 0
        self.bgX1 = 0

        self.bgY2 = -self.rectBGimage.height
        self.bgX2 = 0

        # background speed along the y-axis - changing images
        self.moveSpeed = 5

# background class is able to swith onece going deeper into game
    def update(self):
        self.bgY1 += self.moveSpeed
        self.bgY2 += self.moveSpeed

        # when the background would change
        if self.bgY1>self.rectBGimage.height:
            self.bgY1 = -self.rectBGimage.height

        if self.bgY2>self.rectBGimage.height:
            self.bgY2 = -self.rectBGimage.height
    
    # window switch using two other bg imgs
    def render(self):
        window.blit(self.backgroundImage,(self.bgX1, self.bgY1))
        window.blit(self.backgroundImage,(self.bgX2, self.bgY2))

# instantiaing background
background = Background()

# use a timer to increase speed at certain times
INCREASE_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INCREASE_SPEED, 3000)

        
# projectiles in game - 3 mobs - 1 player
P1 = Player()
E1 = Enemy()
E2 = Enemy()
E3 = Enemy()
B1 = Bullet(P1)

# instantiating enemy players class
enemyGroup = pygame.sprite.Group()
enemyGroup.add(E1)
enemyGroup.add(E2)
enemyGroup.add(E3)

# instantianing bullets class
bullets = pygame.sprite.Group()
bullets.add(B1)


# font style
font = pygame.font.SysFont("Verdana", 40)
# displayed message for game ending
gameOver = font.render("Game Over", True, black)

# initial score displayed 
score = 0
destroyed = False

# while loop to update score when progressing
while True:
    # score +1 everytime wave of aestroids are passed
    scoreRender = font.render("Score: " +str(score), True, red)
    background.update()
    background.render()
    window.blit(scoreRender, (0,0))

    
    # event is when the player makes contact with aestroid entity ending the game
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        # increase in speed of enemy class (aestroids) getting deeper in game
        if event.type == INCREASE_SPEED:
            speed+= 0.5

    # establish a function to quit after play collides with entities 
    if pygame.sprite.spritecollideany(P1, enemyGroup):
        window.fill(red)
        window.blit(gameOver, (100,300))
        pygame.display.update()
        time.sleep(2)
        # quit after game over 
        pygame.quit()

    for entity in bullets:
        # player 1 (spaceship) bullet release
        entity.fire(P1)

    # for loop to create enemy collision with bullet
    for enemy in enemyGroup:
        # when bullets collide aestroids get desroyed
        if pygame.sprite.spritecollide(enemy, bullets, False):
            destroyed = True
            # increase score
            score = score + 3
            enemy.move(score, destroyed)
            window.blit(enemy.image, enemy.rect)
            B1.resetPos()
            destroyed = False

    # aestroid        
    for enemy in enemyGroup:
        # score increase as aestroids dodged
        score = enemy.move(score, destroyed)
        enemy.draw(window)

    P1.update()
    P1.draw(window)

    pygame.display.update()
    framesPerSec.tick(FPS)














    
            
            

    














    
        
    