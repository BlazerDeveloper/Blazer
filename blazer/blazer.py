import sys
import pygame
import vector
import os
from pygame.locals import *

DIVISION = 2
TUX_STARTING_LOC = (700, 300)
NOTHING = (-1, -1)
tux_loc = (700, 300)
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 600
MOVEMENT_SPEED = 5
BACKGROUND1CENTER = (400, 300)
vx = (0, 0)
vy = (0, 0)
FACING_FORWARD = 0
FACING_RIGHT = 1
FACING_DOWN = 2
FACING_LEFT = 3
FACING_UPLEFT = 4
FACING_DWNLEFT = 5
FACING_UPRIGHT = 6
FACING_DWNRIGHT = 7

facing_files = ["tux.png", "tuxright.png", "tuxdown.png", "tuxleft.png", 'tuxupleft.png', 'tuxdwnleft.png',
                'tuxupright.png', 'tuxdwnright.png']


def load_image(filename):
    return pygame.image.load(os.path.join("resources", filename))


class Titlescreen:
    def __init__(self):
        self.running = True

        self.button = load_image('Startbutton.png')
        self.buttonRect = self.button.get_rect(centerx=400, centery=400)

        self.title = load_image("Title.png")
        self.titleRect = self.title.get_rect(centerx=400, centery=200)

        self.button2 = load_image('Quitbutton.png')
        self.button2Rect = self.button.get_rect(centerx=400, centery=500)


    def handle_input(self):
        mousePos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and self.button2Rect.collidepoint(mousePos):
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and self.buttonRect.collidepoint(mousePos):
                self.running = False
            if self.buttonRect.collidepoint(mousePos):
                self.button = load_image("Startbuttonp.png")


    def draw(self):
        screen.fill((0, 255, 0))
        screen.blit(self.title, self.titleRect)
        screen.blit(self.button, self.buttonRect)
        screen.blit(self.button2, self.button2Rect)


    def run(self):
        while self.running:
            self.handle_input()
            self.draw()
            pygame.display.flip()


def do_ingame():
    running = True

    def init():
        # do all your image loading for the game here
        pass

    def draw():
        tux_loc = vector.adding(tux_loc, vector.adding(vx, vy))
        camera_corner = vector.subtracting(tux_loc, half_screen)
        camera_rect = pygame.Rect(camera_corner, size)
        clamped_camera_rect = camera_rect.clamp(background1.get_rect())
        screen.blit(background1, vector.subtracting((0, 0), camera_corner))
        screen.blit(tux, vector.subtracting(tux_loc, clamped_camera_rect.topleft))
        screen.blit(walltop, vector.subtracting((5, 5), camera_corner))
        pygame.display.flip()

    def handle_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_w:
                    vy = (0, -MOVEMENT_SPEED)
                elif event.key == K_s:
                    vy = (0, MOVEMENT_SPEED)
                elif event.key == K_a:
                    vx = (-MOVEMENT_SPEED, 0)
                elif event.key == K_d:
                    vx = (MOVEMENT_SPEED, 0)
            if event.type == KEYUP:
                if event.key == K_w:
                    vy = (0, 0)
                if event.key == K_s:
                    vy = (0, 0)
                if event.key == K_a:
                    vx = (0, 0)
                if event.key == K_d:
                    vx = (0, 0)

            if vx > (0, 0):
                if vy > (0, 0):
                    tux = facings[FACING_DWNRIGHT]
                elif vy < (0, 0):
                    tux = facings[FACING_UPRIGHT]
                else:
                    tux = facings[FACING_RIGHT]
            elif vx < (0, 0):
                if vy > (0, 0):
                    tux = facings[FACING_DWNLEFT]
                elif vy < (0, 0):
                    tux = facings[FACING_UPLEFT]
                else:
                    tux = facings[FACING_LEFT]
            else:
                if vy > (0, 0):
                    tux = facings[FACING_DOWN]
                elif vy < (0, 0):
                    tux = facings[FACING_FORWARD]


    facings = [load_image(x) for x in facing_files]
    background1 = load_image('background1.png')
    background1_rect = background1.get_rect(centerx=400, centery=300)
    half_screen = vector.dividing(DISPLAY_SIZE, DIVISION)

    walltop = load_image("walltop.png")
    walltop_size = pygame.Surface.get_size(walltop)
    walltop_rect = walltop.get_rect(walltop_size)

    tux = facings[FACING_DOWN]
    tux_rect = tux.get_rect(TUX_STARTING_LOC)

    # this is the main loop for the game
    init()
    while running:
        handle_input()
        draw()
        pygame.display.flip()


if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode(DISPLAY_SIZE)
    icon = load_image("Icon.png")

    pygame.display.set_caption("Blazer: Trails Unknown")
    pygame.display.set_icon(icon)
    pygame.display.toggle_fullscreen()

    do_titlescreen()
    do_ingame()