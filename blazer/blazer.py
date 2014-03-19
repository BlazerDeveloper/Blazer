import sys
import pygame
import vector
from pygame.locals import *

DIVISION = 2
TUX_STARTING_LOC = (700, 300)
NOTHING = (-1, -1)
tux_loc = (700, 300)
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 800, 600
MOVEMENT_SPEED = 5
BACKGROUND1CENTER = (400,300)
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

facing_files = ["tux.png","tuxright.png","tuxdown.png","tuxleft.png",'tuxupleft.png','tuxdwnleft.png','tuxupright.png','tuxdwnright.png']

pygame.init()
def load_image(filename):
    return pygame.image.load(os.path.join ("resources",filename))

Icon = load_image("Icon.png")
pygame.display.set_caption("Blazer: Trails Unknown")
pygame.display.set_icon(Icon)

facings = [ load_image(x) for x in facing_files]
screen = pygame.display.set_mode(DISPLAY_SIZE) 
background1= load_image('background1.png')
background1_rect = background1.get_rect(centerx=400, centery=300)
half_screen = vector.dividing(DISPLAY_SIZE, DIVISION)

walltop = load_image("walltop.png")
walltop_size = pygame.Surface.get_size(walltop)
walltop_rect = walltop.get_rect(walltop_size)

tux = facings[FACING_DOWN]
tux_rect = tux.get_rect(TUX_STARTING_LOC)

button = load_image('Startbutton.png')
buttonRect = button.get_rect(centerx=400, centery=400)

title = load_image("title.png")
titleRect = title.get_rect(centerx=400, centery=200)

button2 = load_image('Quitbutton.png')
button2Rect = button.get_rect(centerx=400, centery=500)

buttonp = load_image("startbuttonp.png")

pygame.display.flip()

def do_titlescreen():
    running = True
    def handle_titlescreen_input():
        for event in pygame.event.get():
                    mousePos = pygame.mouse.get_pos()
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN and button2Rect.collidepoint(mousePos):
                        sys.exit()
                    if event.type == buttonRect.collidepoint(mousePos):
                        button = pygame.image.load(os.path.join("resources",'startbuttonp.png'))
                    if event.type == MOUSEBUTTONDOWN and buttonRect.collidepoint(mousePos):
                        running = False
                    else:
                        if event.type == buttonRect.collidepoint(mousePos):
                            screen.blit(buttonp)
        return running
    def draw_titlescreen():
        running = True
        while running:
                pygame.display.toggle_fullscreen()
                screen.fill((0, 255, 0))
                screen.blit(title, titleRect)
                screen.blit(button, buttonRect)
                screen.blit(button2, button2Rect)
                pygame.display.update()

def do_titlescreen():
    running = True

    def init():
        # do all the loading for your titlescreen here
        pass

    def handle_input():
        for event in pygame.event.get():
            mousePos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and button2Rect.collidepoint(mousePos):
                sys.exit()
            if event.type == buttonRect.collidepoint(mousePos):
                button = pygame.image.load('startbuttonp.png')
            if event.type == MOUSEBUTTONDOWN and buttonRect.collidepoint(mousePos):
                running = False
            else:
                if event.type == buttonRect.collidepoint(mousePos):
                    button = pygame.image.load("startbuttonp.png")

    def draw():
        pygame.display.toggle_fullscreen()
        screen.fill((0, 255, 0))
        screen.blit(title, titleRect)
        screen.blit(button, buttonRect)
        screen.blit(button2, button2Rect)
        pygame.display.update()

    # the main loop for the titlescreen
    init()
    while running:
        handle_input()
        draw()


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
        screen.blit(background1, vector.subtracting((0,0), camera_corner))
        screen.blit(tux, vector.subtracting(tux_loc, clamped_camera_rect.topleft))
        screen.blit(walltop, vector.subtracting((5,5),camera_corner))
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

        # this is the main loop for the game
        init()
        while running:
            handle_input()
            draw()

if __name__ == "__main__":
    do_titlescreen()
    do_ingame()
