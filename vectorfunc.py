import sys

import pygame
from pygame.locals import *

pygame.init()

fps = 1
fpsClock = pygame.time.Clock()

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)

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

    print(line, head_centre, head_normal)

    point1 = head - head_centre + head_normal
    point2 = head - head_centre - head_normal

    # Draw line
    pygame.draw.aaline(screen, colour, tail, head)

    # Draw arrow head
    pygame.draw.aaline(screen, colour, point1, head)
    pygame.draw.aaline(screen, colour, point2, head)

# Game loop.
while True:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Update.

    # Draw.
    ## Draw axes
    pygame.draw.line(screen, BLACK, (width/2, 0), (width/2, height))
    draw_arrow(BLACK, (width/2 +10, 0), (width, height))

    pygame.display.flip()
    fpsClock.tick(fps)
