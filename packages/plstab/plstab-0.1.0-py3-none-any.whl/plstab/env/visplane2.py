import numpy as np
import pygame
import random
import os

from pygame.locals import (
    KEYDOWN,
    K_ESCAPE,
    QUIT,
    RLEACCEL,
)

class Player(pygame.sprite.Sprite): # player
    def __init__(self):
        super(Player, self).__init__()
        p = os.path.join(os.path.dirname(__file__), "assets/f35.png")
        self.surf_orig = pygame.image.load(p).convert()
        self.surf_orig.set_colorkey((0, 0, 0), RLEACCEL)
        self.surf = self.surf_orig.copy()
        self.rect = self.surf.get_rect()

    def update(self, x, y, phi):
        self.rotate((x, y), phi)

    def rotate(self, pos, angle):

        w, h = self.surf_orig.get_size()
        originPos = (w // 2, h // 2)
        # offset from pivot to center
        image_rect = self.surf_orig.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        
        # roatated offset from pivot to center
        rotated_offset = offset_center_to_pivot.rotate(-angle)

        # roatetd image center
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)

        # get a rotated image
        rotated_image = pygame.transform.rotate(self.surf_orig, angle)
        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)

        self.surf = rotated_image
        self.rect = rotated_image_rect

        

class Cloud(pygame.sprite.Sprite):
    def __init__(self, sw, sh):
        super(Cloud, self).__init__()
        p = os.path.join(os.path.dirname(__file__), f"assets/c{np.random.randint(0, 4)}.png")
        self.surf = pygame.image.load(p).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(center=(
            random.randint(sw + 20, sw + 100),
            random.randint(0, sh)
        ))
    
    def update(self, vx, vy):
        self.rect.move_ip(-vx, vy)
        if self.rect.right < 0:
            self.kill()



class PlaneVisualizer:
    def __init__(self, s_w=800, s_h=600):
        self.SCREEN_WIDTH = s_w
        self.SCREEN_HEIGHT = s_h

        pygame.init()
        self.clock = pygame.time.Clock()

        SCREEN_WIDTH = 800
        SCREEN_HEIGHT = 600

        self.sw = SCREEN_WIDTH
        self.sh = SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.running = True

        self.ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDCLOUD, 1000)
        self.player = Player() # init player's surface
        self.clouds = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.player.rect.move_ip(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2
        self.phi = 0
        
    def step(self, rx, ry, vx, vy, rphi):

        vx = int(vx//8)
        vy = int(vy//8)

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    self.close()
            elif event.type == QUIT:
                running = False
                self.close()

            elif event.type == self.ADDCLOUD:
                new_cloud = Cloud(self.sw, self.sh)
                self.clouds.add(new_cloud)
                self.all_sprites.add(new_cloud)

        self.phi = int(rphi)
        self.screen.fill((135, 206, 250))
        self.player.update(self.x, self.y, self.phi)
        self.clouds.update(vx, vy)

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect.topleft)

        pygame.display.flip()
        self.clock.tick(100)

    def close(self):
        pygame.quit()



if __name__ == '__main__':
    pv = PlaneVisualizer()
    running = True
    for i in range(3000):
        t = np.random.randint(0, 50)
        pv.step(np.sin(t), np.cos(t), random.randint(30, 50), 1,  int(t * 0.05)) # func get x, y, vx, vy, phi
        