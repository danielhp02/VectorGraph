import sys

import pygame
from pygame.locals import *

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)

# Fonts
latin_roman_italic = 'Resources\Fonts\Latin-Modern-Roman\lmroman10-italic.otf' #'./Resources/Fonts/Latin-Roman-Modern/lmroman10-italic.otf'

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

def draw_arrow(colour, head_pos, tail_pos):
    head = pygame.Vector2(head_pos)
    tail = pygame.Vector2(tail_pos)
    line = pygame.Vector2(head[0] - tail[0], head[1] - tail[1])

    head_centre = pygame.Vector2(line)
    head_centre.scale_to_length(15)

    head_normal = line.rotate(90)
    head_normal.scale_to_length(5)

    #print(line, head_centre, head_normal)

    point1 = head - head_centre + head_normal
    point2 = head - head_centre - head_normal

    # Draw line
    pygame.draw.aaline(screen, colour, tail, head)

    # Draw arrow head
    pygame.draw.aaline(screen, colour, point1, head)
    pygame.draw.aaline(screen, colour, point2, head)

def draw_axes():
    # Initialise Arial font at size 30
    font = pygame.font.Font(latin_roman_italic, 25)

    # Draw x axis
    draw_arrow(BLACK, (width, height/2), (0, height/2))
    x_axis_label = font.render('x', True, BLACK)
    screen.blit(x_axis_label, (width-25, height/2-40))

    # Draw y axis
    draw_arrow(BLACK, (width/2, 0), (width/2, height))
    y_axis_label = font.render('y', True, BLACK)
    screen.blit(y_axis_label, (width/2+10, -10))

# Game loop.
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.

    # Draw.
    draw_axes()

    pygame.display.flip()
    fpsClock.tick(fps)
