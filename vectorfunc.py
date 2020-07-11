import sys
import math
import sympy as sy

import pygame
from pygame.locals import *
import pygame.gfxdraw

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

# Colours
BLACK = (0,0,0)
WHITE = (255,255,255)

# Fonts
latin_roman_italic = 'Resources\Fonts\Latin-Modern-Roman\lmroman10-italic.otf' #'./Resources/Fonts/Latin-Roman-Modern/lmroman10-italic.otf'

# Set up output window
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

origin = (width/2, height/2)

# Symbols for maths functions
t  = sy.symbols('t')

def draw_arrow(colour, head_pos, tail_pos):
    head = pygame.Vector2(head_pos)
    tail = pygame.Vector2(tail_pos)
    line = pygame.Vector2(head[0] - tail[0], head[1] - tail[1])

    if line.magnitude() != 0:
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

class Function:
    def __init__(self, f, domain, t, inclusivity=[0,0]):
        """
        f is a parametric/vector function. Best explained by example, the following
        when passed would result in a circle of radius 50px to be drawn.
        def f(t):
            x = 50 * sy.cos(t)
            y = 50 * sy.sin(t)
            if type(t) is sy.Symbol:
                return (x, y)
            return pygame.Vector2(x, y)
        """

        self.f = f
        self.domain = domain # List containing start and end t-values
        self.inclusivity = inclusivity # a list containing two values, 1 or 0 indicating inclusivity of domain, default [0,0]
        self.precision = 0.01 # replace with something based on frametime

        self.time = self.domain[0] # for drawing vectors

        # Get velocity function
        self.velocity = (sy.diff(self.f(t)[0], t), sy.diff(self.f(t)[1], t))
        print(self.velocity[0])

    # Convert to pixel coordinates (uses math because faster)
    # Give a point relative to origin and get a point relative to display
    def get_coords(self, point):
        return (math.floor(point[0] + origin[0]),
                math.floor(-point[1] + origin[1])) # Y-value sign flipped to have the positive y-direction to be up

    def plot_path(self):
        a = self.domain[0]
        while a <= self.domain[1]: # while loop with hundreds of iterations = bad performance
            point = self.f(a)
            coords = self.get_coords(point)

            # Draw point if in display
            if coords[0] >= 0 and coords[0] <= width:
                if coords[1] >= 0 and coords[1] <= height:
                    pygame.gfxdraw.pixel(screen, coords[0], coords[1], BLACK)

            a += self.precision

    # Trying plot_vectors as a seperate function to allow for optimising plot_path in future
    def plot_vectors(self, *args):
        # *args should be a list of strings containing additional drawing options such as "position", velocity" or "acceleration"

        if self.time > self.domain[1]:
            self.time = self.domain[0]

        point = self.get_coords(self.f(self.time))

        if "position" in args:
            draw_arrow(BLACK, point, origin)

        if "velocity" in args:
            v = (self.velocity[0].subs(t, self.time), self.velocity[1].subs(t, self.time))
            draw_arrow(BLACK, (point[0] + v[0], point[1] - v[1]), point)

        self.time += 1

def f(t):
    x = 50 * sy.cos(t)
    y = 50 * sy.sin(t)
    if type(t) is sy.Symbol:
        return (x, y)
    return pygame.Vector2(x, y)

def r(t):
    x = t
    y = 0.01*t**2
    if type(t) is sy.Symbol:
        return (x, y)
    return pygame.Vector2(x, y)

circle = Function(f, [0, 2*sy.pi], t, [1,1])
parabola = Function(r, [-50, 150], t, [1,1])

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
    circle.plot_path()
    # parabola.plot_path()

    circle.plot_vectors("position", "velocity")
    # parabola.plot_vectors("position", "velocity")

    pygame.display.flip()
    fpsClock.tick(fps)
