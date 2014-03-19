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

facings = [ pygame.image.load(os.path.join("resources","tux.png")), pygame.image.load(os.path.join("resources","tuxright.png")), pygame.image.load(os.path.join("resources","tuxdown.png")), pygame.image.load(os.path.join("resources","tuxleft.png")), pygame.image.load(os.path.join("resources","tuxupleft.png")), pygame.image.load(os.path.join("resources","tuxdwnlft.png")), pygame.image.load(os.path.join("resources","tuxupright.png")), pygame.image.load(os.path.join("resources","tuxdownright.png"))]

screen = pygame.display.set_mode(DISPLAY_SIZE) 
background1= pygame.image.load(os.path.join("resources",'background1.png'))
background1_rect = background1.get_rect(centerx=400, centery=300)
half_screen = vector.dividing(DISPLAY_SIZE, DIVISION)

walltop = pygame.image.load(os.path.join("resources","walltop.png"))
walltop_size = pygame.Surface.get_size(walltop)
walltop_rect = walltop.get_rect(walltop_size)

tux = facings[FACING_DOWN]
tux_rect = tux.get_rect(TUX_STARTING_LOC)


button = pygame.image.load(os.path.join("resources",'Startbutton.png'))
buttonRect = button.get_rect(centerx=400, centery=400)

title = pygame.image.load(os.path.join("resources","title.png"))
titleRect = title.get_rect(centerx=400, centery=200)

button2 = pygame.image.load(os.path.join("resources",'Quitbutton.png'))
button2Rect = button.get_rect(centerx=400, centery=500)

buttonp = pygame.image.load(os.path.join("resources","startbuttonp.png"))

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

    while running:
        handle_titlescreen_input()
        draw_titlescreen()

def do_ingame():
    running = True
    
    def draw_ingame():           
        tux_loc = vector.adding(tux_loc, vector.adding(vx, vy))
        camera_corner = vector.subtracting(tux_loc, half_screen)
        camera_rect = pygame.Rect(camera_corner, size)
        clamped_camera_rect = camera_rect.clamp(background1.get_rect())
        screen.blit(background1, vector.subtracting((0,0), camera_corner))
        screen.blit(tux, vector.subtracting(tux_loc, clamped_camera_rect.topleft))
        screen.blit(walltop, vector.subtracting((5,5),camera_corner))
        pygame.display.flip()
        
    def handle_ingame_input():
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

    while running:
        do_ingame()