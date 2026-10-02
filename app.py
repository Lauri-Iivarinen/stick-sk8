# Example file showing a basic pygame "game loop"
import pygame
from Skateboard import Skateboard
from Background import Background
from Dude import Dude

HEIGHT = 1000
WIDTH = 1000

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1200, 900))
overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
clock = pygame.time.Clock()
running = True

# CONST
JUMP_SPEED = 5

# Classes
sb = Skateboard(screen, -210, 726, JUMP_SPEED)
bg = Background(screen, 1400, 750, overlay)
dude = Dude(screen, -145, 200, JUMP_SPEED) # 65px ahead of deck

sbt = Skateboard(screen, 500, 726, JUMP_SPEED)

animations = [
    sb.idle_30, 
    sb.idle_30, 
    sb.roll_to_view, 
    sb.ollie_2,
    sb.ollie_2, 
    sb.idle, 
    sb.infinite_board
]
background = [
    bg.draw_cloud
]
floor = [
    bg.start_floor, 
    bg.idle_40, 
    bg.idle_20, 
    bg.phase1, 
    bg.infinite_floor
]
bgt = [bg.infinite_floor]
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
    continue_animation(floor)
    #continue_animation(characters)
    continue_animation(background)

    #sbt.ollie_2()
    #bg.infinite_floor()

    bg.fade()

    screen.blit(overlay, (0, 0))
    pygame.display.flip()
    clock.tick(30)  # limits FPS to 30
    i += 0.2

pygame.quit()