'''
ASSET CREDITS
doux.png, tard.png - https://arks.itch.io/dino-characters?download
birb.png - https://foozlecc.itch.io/little-bird 
'''

import pygame
from spritesheet import SpriteSheet, SpriteState
from transparent_window import TRANSPARENT, set_window_transparent, get_taskbar_height

pygame.init()
vec = pygame.math.Vector2

FULLSCREEN = (0, 0)
scr = pygame.display.set_mode(FULLSCREEN, pygame.NOFRAME)
SCR_W, SCR_H = pygame.display.get_surface().get_size()

FPS = 60
FLOOR = SCR_H - get_taskbar_height()

BLACK = (0, 0, 0)

# create layered transparent window
set_window_transparent()

# load assets
dino_spritesheet_image = pygame.image.load('assets/tard.png').convert_alpha()
dino_spritesheet = SpriteSheet(dino_spritesheet_image, 24, BLACK)

birb_spritesheet_image = pygame.image.load('assets/birb.png').convert_alpha()
birb_spritesheet = SpriteSheet(birb_spritesheet_image, 64, BLACK)

class Dino(pygame.sprite.Sprite):
    FRIC = -0.08
    ACC = 1
    
    def __init__(self, spritesheet, x, y):
        super().__init__()
        self.spritesheet = spritesheet
        self.current_sprite = 0
        self.sprite_states = {'idle': SpriteState(4, 0), 'run': SpriteState(7, 17)}  # [count, start_idx]
        self.state = 'idle'
        self.isRight = True
        
        self.image = self.get_frame()
        
        self.pos = vec((x, y))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        self.active = False
        
        self.rect = self.image.get_rect()
        self.floor = FLOOR - self.rect.height/2 + 6  # adjust for sprite
        self.pos.y = self.floor        
        self.rect.center = self.pos
        
    def get_frame(self):
        sprite_state_factor = self.sprite_states[self.state].idx
        return self.spritesheet.get_image(int(self.current_sprite) + sprite_state_factor, 3, right=self.isRight)
    
    def update(self, speed):
        self.acc = vec(0, 0)
        if self.active:
            # key presses
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:  # left
                self.isRight = False
                self.state = 'run'
                self.acc.x = -self.ACC
            elif pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:  # right
                self.isRight = True
                self.state = 'run'
                self.acc.x = self.ACC
            else:
                self.state = 'idle'
                
            # movement
            self.acc.x += self.vel.x * self.FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.3 * self.acc
            
            # bounds
            if self.pos.x > SCR_W:
                self.pos.x = SCR_W
            elif self.pos.x < 0:
                self.pos.x = 0
            
            # update position
            self.rect.center = self.pos
        
        # animation loop
        self.current_sprite += speed
        if int(self.current_sprite) >= self.sprite_states[self.state].count:
            self.current_sprite = 0
        self.image = self.get_frame()
        

class Bird(pygame.sprite.Sprite):
    FRIC = -0.08
    ACC = 0.3
    GRAV = 9.81/60
    UP = -1.5
    MAX_VEL_Y = 7
    def __init__(self, spritesheet, x, y):
        super().__init__()    
        self.spritesheet = spritesheet
        self.current_sprite = 0
        self.sprite_states = {'idle': SpriteState(5, 0), 'walk': SpriteState(8, 1), 'jump': SpriteState(6, 2), 'glide':SpriteState(4, 6), 'fly-fwd':SpriteState(4, 4), 'fly-up':SpriteState(4, 5)} 
        self.state = 'idle'
        self.isRight = True
        
        self.image = self.get_frame()
        
        self.active = True
        
        self.flap_released = True
        self.flapping_count = 0
        
        self.pos = vec((x, y))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.floor = FLOOR - self.rect.height/2 + 72
    
    def get_frame(self):
        return self.spritesheet.get_image(int(self.current_sprite), 3, state=self.sprite_states[self.state].idx, right=self.isRight)
    
    def update(self, speed):
        self.acc = vec(0,0)
        if self.active:
            # key presses
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_a] or pressed_keys[pygame.K_LEFT]:  # left
                self.isRight = False
                self.state = 'walk' if self.pos.y == self.floor else 'fly-fwd'
                self.acc.x = -self.ACC
            elif pressed_keys[pygame.K_d] or pressed_keys[pygame.K_RIGHT]:  # right
                self.isRight = True
                self.state = 'walk' if self.pos.y == self.floor else 'fly-fwd'
                self.acc.x = self.ACC
            else:
                self.state = 'idle' if self.pos.y == self.floor else 'glide'
            
            if (pressed_keys[pygame.K_SPACE] or pressed_keys[pygame.K_w] or pressed_keys[pygame.K_UP]) and self.flapping_count == 0 and self.flap_released:  # up
                self.flapping_count = 22
                self.flap_released = False
                
            if self.flapping_count > 0:
                if self.flapping_count > 16:  # only up accel for 6 frames
                    self.acc.y = self.UP
                # continue fly-up animation past up accel
                self.flapping_count -= 1
                self.state = 'fly-up'
            # movement
            self.acc.x += self.vel.x * self.FRIC * (0.3 + 0.7*(self.pos.y == self.floor))
            self.vel.x += self.acc.x

            self.acc.y += self.GRAV
            self.vel.y = max(-self.MAX_VEL_Y, min(self.vel.y + self.acc.y, self.MAX_VEL_Y))

            self.pos += self.vel + 0.3 * self.acc
            # bounds 
            if self.pos.x > SCR_W:
                self.pos.x = SCR_W
            elif self.pos.x < 0:
                self.pos.x = 0
            if self.pos.y > self.floor:
                self.pos.y = self.floor
                self.acc.y = 0
                self.vel.y = 0
            
        # update position
        self.rect.center = self.pos
        
        # animation loop
        self.current_sprite += speed
        if int(self.current_sprite) >= self.sprite_states[self.state].count:
            self.current_sprite = 0
        self.image = self.get_frame()

def main():
    clock = pygame.time.Clock()
    run = True
    
    actors = pygame.sprite.Group()
    dino = Dino(dino_spritesheet, 80, 0)
    actors.add(dino)

    birb = Bird(birb_spritesheet, 100, 50)
    actors.add(birb)
    
    while run:
        clock.tick(FPS)
        # event handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE or event.key == pygame.K_w or event.key == pygame.K_UP:
                    birb.flap_released = True
        
        # update background
        scr.fill(TRANSPARENT)  # transparent background
        # draw stuff
        actors.draw(scr)
        actors.update(0.2)
        # pygame.draw.rect(scr, 'red', birb.rect, width=2)
        pygame.display.update()
        
main()