from setteing import *

class Sprites(pygame.sprite.Sprite):
    def __init__(self,pos,surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,collisions, *groups):
        super().__init__(*groups)
        self.image = pygame.image.load(join('images','player','0.png')).convert_alpha()
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2()
        self.speed = 1000
        self.collisions_sprites = collisions

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
    
    def move(self,dt):
        self.rect.centerx += self.speed * self.direction.x * dt
        self.collisions('horizontal')
        self.rect.centery += self.speed * self.direction.y * dt
        self.collisions('vertical')
    
    def collisions(self,dir):
        for sprite in self.collisions_sprites:
            if sprite.rect.colliderect(self.rect):
                if dir == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                else:
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom

    def update(self, dt):
        self.input()
        self.move(dt)