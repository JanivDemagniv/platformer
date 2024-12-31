from setteing import *
from timer import Timer

class Sprites(pygame.sprite.Sprite):
    def __init__(self,pos,surf, *groups):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft=pos)
        self.ground = True

class Bullet(Sprites):
    def __init__(self, pos, surf, direction, *groups):
        super().__init__(pos, surf, *groups)

        #adjusment
        self.image = pygame.transform.flip(self.image,direction == -1 , False)

        #movement
        self.direction = direction
        self.speed = 850
    
    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fire(Sprites):
    def __init__(self, pos, surf, player, *groups):
        super().__init__(pos, surf, *groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100,autoStart = True, func= self.kill)
        self.y_offset = pygame.Vector2(0,8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image,True,False)
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset
    
    def update(self,_):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()

class AnimatedSprites(Sprites):
    def __init__(self, pos, frames, groups):
        self.frames,self.frame_index,self.animation_speed = frames,0,10
        super().__init__(pos, self.frames[int(self.frame_index)], groups)
    
    def animate(self,dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Player(AnimatedSprites):
    def __init__(self,pos,frames,collisions, create_bullet, *groups):
        super().__init__(pos,frames,*groups)
        
        self.flip = False

        self.direction = pygame.Vector2()
        self.speed = 400
        self.collisions_sprites = collisions
        self.gravity = 50
        self.on_floor = False

        #shoot
        self.create_bullet = create_bullet

        #timer
        self.shoot_timer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        if keys[pygame.K_UP] and self.on_floor:
            self.direction.y = - 20
        
        if keys[pygame.K_SPACE] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()
    
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
        self.shoot_timer.update()
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