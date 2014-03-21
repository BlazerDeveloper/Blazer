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
FACING_FORWARD = 0
FACING_RIGHT = 1
FACING_DOWN = 2
FACING_LEFT = 3
FACING_UPLEFT = 4
FACING_DWNLEFT = 5
FACING_UPRIGHT = 6
FACING_DWNRIGHT = 7

facing_files = ["tux.png", "tuxright.png", "tuxdown.png", "tuxleft.png", 'tuxupleft.png', 'tuxdwnlft.png',
                'tuxupright.png', 'tuxdownright.png']


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
            if not self.buttonRect.collidepoint(mousePos):
                self.button = load_image("startbutton.png")

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
class TuxSprite(pygame.sprite.Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = load_image("tux.png")
        self.rect = self.image.get_rect()
class WallSprite(pygame.sprite.Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = load_image("walltop.png")
        self.rect = self.image.get_rect()
class Ingame:
    def __init__(self):
        self.running = True
        self.facings = [load_image(x) for x in facing_files]
        self.background1 = load_image('background1.png')
        self.background1_rect = self.background1.get_rect(centerx=400, centery=300)
        self.half_screen = vector.dividing(DISPLAY_SIZE, DIVISION)
        self.walltop = load_image("walltop.png")
        self.tux = self.facings[FACING_DOWN]
        self.tux_rect = self.tux.get_rect(x = 700, y = 300)
        self.walltop_rect = self.walltop.get_rect(centerx = 400, centery = 100)
        self.vx = (0, 0)
        self.vy = (0, 0)
        self.tux_loc = (700, 300)
        self.DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 600

    def draw(self):
        self.tux_loc = vector.adding(self.tux_loc, vector.adding(self.vx, self.vy))
        self.camera_corner = vector.subtracting(self.tux_loc, self.half_screen)
        self.camera_rect = pygame.Rect(self.camera_corner, self.DISPLAY_SIZE)
        self.clamped_camera_rect = self.camera_rect.clamp(self.background1.get_rect())
        screen.blit(self.background1, vector.subtracting((0, 0), self.camera_corner))
        screen.blit(self.tux, vector.subtracting(self.tux_loc, self.clamped_camera_rect.topleft))
        screen.blit(self.walltop, vector.subtracting((5, 5), self.camera_corner))
        pygame.display.flip()
    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
                elif event.key == K_w:
                    self.vy = (0, -MOVEMENT_SPEED)
                elif event.key == K_s:
                    self.vy = (0, MOVEMENT_SPEED)
                elif event.key == K_a:
                    self.vx = (-MOVEMENT_SPEED, 0)
                elif event.key == K_d:
                    self.vx = (MOVEMENT_SPEED, 0)
            if event.type == KEYUP:
                if event.key == K_w:
                    self.vy = (0, 0)
                if event.key == K_s:
                    self.vy = (0, 0)
                if event.key == K_a:
                    self.vx = (0, 0)
                if event.key == K_d:
                    self.vx = (0, 0)

            if self.vx > (0, 0):
                if self.vy > (0, 0):
                    self.tux = self.facings[FACING_DWNRIGHT]
                elif self.vy < (0, 0):
                    self.tux = self.facings[FACING_UPRIGHT]
                else:
                    self.tux = self.facings[FACING_RIGHT]
            elif self.vx < (0, 0):
                if self.vy > (0, 0):
                    self.tux = self.facings[FACING_DWNLEFT]
                elif self.vy < (0, 0):
                    self.tux = self.facings[FACING_UPLEFT]
                else:
                    self.tux = self.facings[FACING_LEFT]
            else:
                if self.vy > (0, 0):
                    self.tux = self.facings[FACING_DOWN]
                elif self.vy < (0, 0):
                    self.tux = self.facings[FACING_FORWARD]
            print(self.tux_rect)
            if self.tux_rect.colliderect(self.walltop_rect):
                self.tux_loc = (700, 300)
    def run(self):
        while self.running:
            self.handle_input()
            self.draw()
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY_SIZE)
    icon = load_image("Icon.png")
    pygame.display.set_caption("Blazer: Trails Unknown")
    pygame.display.set_icon(icon)
    pygame.display.toggle_fullscreen()

    titlescreen = Titlescreen()
    titlescreen.run()
    ingame = Ingame()
    ingame.run()