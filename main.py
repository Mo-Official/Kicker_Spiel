import random
import pygame as pg
import time

# Define some colors
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
GREEN = ( 0, 255, 0)
RED = ( 255, 0, 0)
BLUE = (0, 0, 255)

PINK = (255, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 155, 0)

pg.init()
size = (1200, 600)
screen = pg.display.set_mode(size)
pg.display.set_caption("Kicker Game")

player_1_goalbox = pg.Rect(0, 125, 200, 350)
player_2_goalbox = pg.Rect(1000, 125, 200, 350)

confetti_rects = [(pg.Rect(600,300, 20, 5), random.choice([PINK, RED, YELLOW, BLUE, ORANGE]), random.randint(-100, 100), random.randint(-100,100)) for _ in range(300)]

# The loop will carry on until the user exits the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pg.time.Clock()

ball = pg.Rect(100, 100, 20, 20)
ball_vel_x = 10
ball_vel_y = 10

show_confetti = False
confetti_timer = 0

class Fig:
    def __init__(self, c, pos) -> None:
        self.c = c
        self.rect = pg.Rect(pos[0],pos[1], 100,50)
        self.dir = 1

class Stick:
    def __init__(self, figs) -> None:
        self.dir = 1
        self.figs = figs
    
    def flip_dir(self):
        self.dir *=-1
        for fig in self.figs:
            fig.rect.x += self.dir * (fig.rect.width//2)
            
    def update_pos(self, y):
        for fig in self.figs:
            fig.rect.y += y
            
    def draw_figs(self, screen):
        for fig in self.figs:
            pg.draw.rect(screen, fig.c, fig.rect)

player_1_sticks = [Stick([Fig(BLUE, (100,275))]),
                   Stick([Fig(BLUE, (450, 275)), Fig(BLUE, (450, 125)), Fig(BLUE, (450, 425))]),
                   Stick([Fig(BLUE, (800, 275)),Fig(BLUE, (800, 125)),Fig(BLUE, (800, 425)), ])]
player_1_selected = 0
player_1_stick_y_vel = 0

player_2_sticks = [Stick([Fig(RED, (1000,275))]),
                   Stick([Fig(RED, (650,275)),Fig(RED, (650,125)),Fig(RED, (650,425)),]),
                   Stick([Fig(RED, (300,275)),Fig(RED, (300,425)),Fig(RED, (300,125))]),]
player_2_selected = 0
player_2_stick_y_vel = 0



# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pg.event.get(): # User did something
        if event.type == pg.QUIT: # If user clicked close
                carryOn = False # Flag that we are done so we can exit the while loop
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_f:
                player_1_sticks[player_1_selected].flip_dir()
            if event.key == pg.K_w:
                player_1_stick_y_vel = -10
            if event.key == pg.K_s:
                player_1_stick_y_vel = 10
            if event.key == pg.K_d:
                player_1_selected = min(player_1_selected+1, 2)
            if event.key == pg.K_a:
                player_1_selected = max(player_1_selected-1, 0)
            if event.key == pg.K_LEFT:
                player_2_selected = min(player_2_selected+1, 2)
            if event.key == pg.K_RIGHT:
                player_2_selected = max(player_2_selected-1, 0) 
            
            if event.key == pg.K_k:
                player_2_sticks[player_2_selected].flip_dir()
            if event.key == pg.K_DOWN:
                player_2_stick_y_vel = 10
            if event.key == pg.K_UP:
                player_2_stick_y_vel = -10   
            
            
        if event.type == pg.KEYUP:
            if event.key == pg.K_w:
                player_1_stick_y_vel = max(player_1_stick_y_vel, 0)
            if event.key == pg.K_s:
                player_1_stick_y_vel = min(player_1_stick_y_vel, 0)
            if event.key == pg.K_UP:
                player_2_stick_y_vel = max(player_2_stick_y_vel, 0)
            if event.key == pg.K_DOWN:
                player_2_stick_y_vel = min(player_2_stick_y_vel, 0)

    # --- Game logic should go here
    ball.x += ball_vel_x
    ball.y += ball_vel_y
    
    if ball.x > 1150 or ball.x < 25:
        ball_vel_x *=-1
    if ball.y > 550 or ball.y < 25:
        ball_vel_y *=-1
    
    for s in player_1_sticks:
        if ball.collidelist([fig.rect for fig in s.figs]) == -1:
            continue
        ball_vel_x *= -1
    
    for s in player_2_sticks:
        if ball.collidelist([fig.rect for fig in s.figs]) == -1:
            continue
        ball_vel_x *= -1
    
        
    if (ball.x >= 1150 and ball.colliderect(player_2_goalbox)) or ball.x <= 50 and ball.colliderect(player_1_goalbox):
        confetti_rects = [(pg.Rect(600,300, 20, 5), random.choice([PINK, RED, YELLOW, BLUE, ORANGE]), random.randint(-100, 100), random.randint(-100,100)) for _ in range(300)]
        show_confetti = True
        confetti_timer = time.time()
        ball.x, ball.y = screen.get_rect().center
    
    player_1_sticks[player_1_selected].update_pos(player_1_stick_y_vel)    
    player_2_sticks[player_2_selected].update_pos(player_2_stick_y_vel)    
    
    if time.time() - confetti_timer > 1:
        show_confetti = False
    
    if show_confetti:    
        for confetti, _, confetti_x, confetti_y in confetti_rects:
            confetti.x += confetti_x/random.randint(3,7)
            confetti.y += confetti_y/random.randint(3,7)
            
    # --- Drawing code should go here
    # First, clear the screen to white. 
    screen.fill(GREEN)
    pg.draw.polygon(screen, WHITE, [(200,300), (1000,300)], 10)
    pg.draw.circle(screen, WHITE, screen.get_rect().center, 200, 10)
    pg.draw.circle(screen, WHITE, screen.get_rect().center, 20, 20)
    pg.draw.rect(screen, WHITE, player_1_goalbox, 10)
    pg.draw.rect(screen, WHITE, player_2_goalbox, 10)
    
    pg.draw.circle(screen, BLUE, ball.center, 15)
    pg.draw.polygon(screen, BLACK, [(0,0), (0,600),(1200,600),(1200,0)], 50)
    pg.draw.line(screen, BLACK, (125, 0), (125,600), 5)
    pg.draw.line(screen, BLACK, (475, 0), (475,600), 5)
    pg.draw.line(screen, BLACK, (825, 0), (825,600), 5)
    pg.draw.line(screen, BLACK, (675, 0), (675,600), 5)
    pg.draw.line(screen, BLACK, (325, 0), (325,600), 5)
    pg.draw.line(screen, BLACK, (1025, 0), (1025,600), 5)
    
    
    if show_confetti:
        for confetti, confetti_color, _, _ in confetti_rects:
            pg.draw.rect(screen, confetti_color, confetti)
    
    
    for s in player_1_sticks:
        s.draw_figs(screen)
    for s in player_2_sticks:
        s.draw_figs(screen)
    # --- Go ahead and update the screen with what we've drawn.
    pg.display.flip()
    
    # --- Limit to 60 frames per second
    clock.tick(30)

    #Once we have exited the main program loop we can stop the game engine:
pg.quit()