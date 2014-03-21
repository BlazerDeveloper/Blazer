import sys
import pygame
import vector
import os
from pygame.locals import *

DIVISION = 2
TUX_STARTING_LOC = (700, 300)
NOTHING = (-1, -1)
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
    facing_files = ["tux.png", "tuxright.png", "tuxdown.png", "tuxleft.png", 'tuxupleft.png', 'tuxdwnlft.png',
                    'tuxupright.png', 'tuxdownright.png']

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("tux.png")
        self.rect = self.image.get_rect(x=700, y=300)
        self.facings = [load_image(x) for x in facing_files]

    def update(self, dt=0):
        pass

    def change_facing(self, vx, vy):
        if vx > (0, 0):
            if vy > (0, 0):
                self.sprite = self.facings[FACING_DWNRIGHT]
            elif vy < (0, 0):
                self.sprite = self.facings[FACING_UPRIGHT]
            else:
                self.sprite = self.facings[FACING_RIGHT]
        elif vx < (0, 0):
            if vy > (0, 0):
                self.sprite = self.facings[FACING_DWNLEFT]
            elif vy < (0, 0):
                self.sprite = self.facings[FACING_UPLEFT]
            else:
                self.sprite = self.facings[FACING_LEFT]
        else:
            if vy > (0, 0):
                self.sprite = self.facings[FACING_DOWN]
            elif vy < (0, 0):
                self.sprite = self.facings[FACING_FORWARD]

class WallSprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image("walltop.png")
        self.rect = self.image.get_rect(centerx=400, centery=100)

    def update(self, dt=0):
        pass

class Ingame:
    def __init__(self):
        self.running = True

        self.background1 = load_image('background1.png')
        self.background1_rect = self.background1.get_rect(centerx=400, centery=300)
        self.half_screen = vector.dividing(DISPLAY_SIZE, DIVISION)

        self.walltop = WallSprite()
        self.tux = TuxSprite()

        self.vx = (0, 0)
        self.vy = (0, 0)

        self.DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 600

    def update(self, dt=0):
        #self.group.update(dt)
        self.tux.rect.center = vector.adding(self.tux.rect.center, vector.adding(self.vx, self.vy))
        if self.tux.rect.colliderect(self.walltop.rect):
            self.tux.rect.center = (700, 300)

    def draw(self):
        camera_corner = vector.subtracting(self.tux.rect.center, self.half_screen)
        camera_rect = pygame.Rect(camera_corner, self.DISPLAY_SIZE)
        clamped_camera_rect = camera_rect.clamp(self.background1.get_rect())

        screen.blit(self.background1, (0, 0), camera_corner)
        screen.blit(self.tux.image, vector.subtracting(self.tux.rect.center, clamped_camera_rect.topleft))
        screen.blit(self.walltop.image, (5, 5), camera_corner)

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

            self.tux.change_facing(self.vx, self.vy)

    def run(self):
        while self.running:
            self.handle_input()
            self.update()
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