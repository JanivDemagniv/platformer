from setteing import *

class Sprites(pygame.sprite.Sprite):
    def __init__(self,pos,surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True

class AnimatedSprites(Sprites):
    def __init__(self, pos, frames, groups):
        self.frames,self.frame_index,self.animation_speed = frames,0,10
        super().__init__(pos, self.frames[int(self.frame_index)], groups)
    
    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Player(AnimatedSprites):
    def __init__(self,pos,frames,collisions, *groups):
        super().__init__(pos,frames,*groups)
        
        self.flip = False

        self.direction = pygame.Vector2()
        self.speed = 400
        self.collisions_sprites = collisions
        self.gravity = 50
        self.on_floor = False

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_SPACE] and self.on_floor:
            self.direction.y = - 20
    
    def move(self,dt):
        #horizontal
        self.rect.x += self.speed * self.direction.x * dt
        self.collisions('horizontal')

        #vertical
        self.direction.y += self.gravity * dt   
        self.rect.y += self.direction.y
        self.collisions('vertical')
    
    def collisions(self,dir):
        for sprite in self.collisions_sprites:
            if sprite.rect.colliderect(self.rect):
                if dir == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if dir == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.FRect((0,0),(self.rect.width,2)).move_to(midtop = self.rect.midbottom)
        level_rects = [sprite.rect for sprite in self.collisions_sprites]
        self.on_floor = True if bottom_rect.collidelist(level_rects) >= 0 else False

    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0 
        else:
            self.frame_index = 0

        self.frame_index = 1 if not self.on_floor else self.frame_index
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image,self.flip,False)

    def update(self, dt):
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)

class Bee(AnimatedSprites):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)

class Worm(AnimatedSprites):
    def __init__(self, pos, frames, groups):
        super().__init__(pos, frames, groups)

    def update(self, dt):
        self.animate(dt)