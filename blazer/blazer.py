import sys, pygame
from pygame.locals import *
import vector

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

pygame.init()
 
Icon = pygame.image.load("Icon.png")
pygame.display.set_caption("Blazer: Trails Unknown")
pygame.display.set_icon(Icon)

facings = [ pygame.image.load("tux.png"), pygame.image.load("tuxright.png"), pygame.image.load("tuxdown.png"), pygame.image.load("tuxleft.png"), pygame.image.load("tuxupleft.png"), pygame.image.load("tuxdwnlft.png"), pygame.image.load("tuxupright.png"), pygame.image.load("tuxdownright.png")]

screen = pygame.display.set_mode(size) 
background1= pygame.image.load('background1.png')
background1_rect = background1.get_rect(centerx=400, centery=300)
half_screen = vector.dividing(size, division)
tux = facings[2]
walltop = pygame.image.load("walltop.png")
walltop_size = pygame.Surface.get_size(walltop)

tux_rect = tux.get_rect(tux_loc)
walltop_rect = walltop.get_rect(walltop_size)

button = pygame.image.load('Startbutton.png')
buttonRect = button.get_rect(centerx=400, centery=400)
title = pygame.image.load("title.png")
titleRect = title.get_rect(centerx=400, centery=200)
button2 = pygame.image.load('Quitbutton.png')
button2Rect = button.get_rect(centerx=400, centery=500)
pygame.display.flip()

start = False
def draw_titlescreen():
    while not start:
                pygame.display.toggle_fullscreen()
                screen.fill((0, 255, 0))
                screen.blit(title, titleRect)
                screen.blit(button, buttonRect)
                screen.blit(button2, button2Rect)
                pygame.display.update()
def handle_titlescreen_input():
    while not start:
        for event in pygame.event.get():
                    mousePos = pygame.mouse.get_pos()
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == MOUSEBUTTONDOWN and button2Rect.collidepoint(mousePos):
                        sys.exit()
                    if event.type == buttonRect.collidepoint(mousePos):
                        button = pygame.image.load('startbuttonp.png')
                    if event.type == MOUSEBUTTONDOWN and buttonRect.collidepoint(mousePos):
                        start = True
                    else:
                        if event.type == buttonRect.collidepoint(mousePos):
                            button = pygame.image.load("startbuttonp.png")
def handle_ingame_input():
    while start:
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
def draw_ingame():           
    while start:
        if walltop_rect.colliderect(tux_rect):
            tux_loc = (600, 400)
        
        tux_loc = vector.adding(tux_loc, vector.adding(vx, vy))
        camera_corner = vector.subtracting(tux_loc, half_screen)
        camera_rect = pygame.Rect(camera_corner, size)
        clamped_camera_rect = camera_rect.clamp(background1.get_rect())
        screen.blit(background1, vector.subtracting((0,0), camera_corner))
        screen.blit(tux, vector.subtracting(tux_loc, clamped_camera_rect.topleft))
        screen.blit(walltop, vector.subtracting((5,5),camera_corner))
        pygame.display.flip()
        
