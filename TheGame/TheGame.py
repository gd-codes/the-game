#________________________________________________________________________________________________________
#
#                                               Game
#--------------------------------------------------------------------------------------------------------
# Code and images obtained from https://github.com/techwithtim/pygame-tutorials and modified
#--------------------------------------------------------------------------------------------------------

import pygame
import random

pygame.init()

# Create screen
scr_size = scrwid, scrht = 500, 480
win = pygame.display.set_mode(scr_size)
pygame.display.set_caption("Game")

# Load images
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

# Game clock
clock = pygame.time.Clock()

# Fonts
small = pygame.font.SysFont('comic sans', 20)
med = pygame.font.SysFont('comic sans', 50)

# Score variable
score = 0


class Player :
    """Creates a player object"""
    
    def __init__(self, x, y, width=64, height=64):        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.jump = False
        self.jumpCount = 10
        

    def draw(self):
        global win
        win.blit(char, (self.x, self.y))
                


class Projectile :
    """ Creates a bullet object"""
    
    def __init__(self, x, y, radius=5, color=(0,0,0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vel = 6

    def draw(self):
        global win
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)



def update_screen():
    """Redraws the game window"""

    global man, bullets, win, score
    
    win.blit(bg, (0,0))
    man.draw()
    for bullet in bullets:
        bullet.draw()
    message("Score : {}".format(score), scrwid*0.8, 20, small)
    
    pygame.display.update()

def message(text, x, y, font, colour=(0,0,0)):
    """Displays text to the screen"""
    abc = font.render(text, True, colour)
    win.blit(abc, (x,y))    

def endgame() :
    """Ends the game"""
    global run
    run = False
    message('Game Over', scrwid/2 - 100, scrht/2, med)
    pygame.display.update()
    pygame.time.delay(3500)
    pygame.quit()


def gameloop():
    """ Main part of the program"""

    global man, bullets, clock, score
    
    man = Player(200, 410)
    bullets = []
    
    update_screen()
    pygame.time.delay(1500)
    
    run = True
    
    while run:
        
        # Check if window is being closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Change bullet position and check if the man is killed
        for bullet in bullets:
            if bullet.x > 0:
                bullet.x -= bullet.vel
                if bullet.x in range(round(man.x), round(man.x + man.width)) and \
                   bullet.y in range(round(man.y), round(man.y + man.height)) :
                    endgame()
            else:
                bullets.pop(bullets.index(bullet))
                score += 1

        # Check for events
        keys = pygame.key.get_pressed()                
            # move man left/right when arrow keys are pressed
        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
        elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
            man.x += man.vel     
            # jump when spacebar is pressed
        if not man.jump :
            if keys[pygame.K_SPACE]:
                man.jump = True
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.5 * neg
                man.jumpCount -= 1
            else:
                man.jump = False
                man.jumpCount = 10
            # stay in the current position if enter is pressed
        if keys[pygame.K_RETURN] :
            man.y = man.y
            man.jump = False

        # Fire bullets randomly
        if random.random() < 0.05 :
            if len(bullets) < 5:
                    bullets.append(Projectile((scrwid + 10), round(man.y + man.height//2)))

        clock.tick(27)
        # Display the changes
        update_screen()


if __name__  == '__main__' :

    print("\n\nGAME INSTRUCTIONS\nIn this game, the man must dodge bullets that are flying at him from\
the right hand edge of the screen. Use the spacebar to jump over incoming bullets or jump down after \
hovering, and the enter key to hover in the current position. You can also use the left and right arrow\
 keys to move left and right. The score is the number of bullets that succesfully pass across the screen\
 without hitting the man. If he is hit, the game ends.")

    gameloop()

    pygame.quit()

#__________________________________________________________________________________________________________
