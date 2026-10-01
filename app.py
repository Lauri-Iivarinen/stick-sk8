# Example file showing a basic pygame "game loop"
import pygame
from Skateboard import Skateboard
from Background import Background
from Dude import Dude

HEIGHT = 1000
WIDTH = 1000

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 1000))
clock = pygame.time.Clock()
running = True

# CONST
JUMP_SPEED = 5

# Classes
sb = Skateboard(screen, -210, 675, JUMP_SPEED)
bg = Background(screen, 1000, 700)
dude = Dude(screen, -145, 200, JUMP_SPEED) # 65px ahead of deck

sbt = Skateboard(screen, 500, 600, JUMP_SPEED)

animations = [
    sb.idle_30, 
    sb.idle_30, 
    sb.idle_30, 
    sb.roll_to_view, 
    sb.ollie_2, 
    sb.idle, 
    sb.ollie_2, 
    sb.idle, 
    sb.infinite_board
]
backgrounds = [
    bg.start_floor, 
    bg.idle_40, 
    bg.idle_15, 
    bg.phase1, 
    bg.infinite_floor
]
characters = [
    dude.idle_40, 
    dude.idle_40, 
    dude.idle_10, 
    dude.roll_to_view, 
    dude.idle_40, 
    dude.idle_5, 
    dude.pop, 
    dude.idle_10, 
    dude.idle_2, 
    dude.pop, 
    dude.infinite_dude
]
#t = [sbt.ollie_2, sbt.idle_20,sbt.ollie_2, sbt.idle_20,sbt.ollie_2, sbt.idle_20,sbt.ollie_2, sbt.idle_20]

def continue_animation(anim: list):
    current_animation = anim[0] if len(anim) > 0 else None
    if current_animation != None:
        if current_animation(): # animation has finished
            anim.pop(0)
            #print("New animation active: ", anim[0])

i = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("white")

    continue_animation(animations)
    continue_animation(backgrounds)
    #continue_animation(characters)

    #sbt.draw()
    #sbt.draw_ollie_nose(i, 170)
    #sbt.ollie_2()
    
    #continue_animation(t)

    pygame.display.flip()
    clock.tick(30)  # limits FPS to 30
    i += 0.2

pygame.quit()