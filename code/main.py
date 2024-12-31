from setteing import *
from sprites import *
from groups import AllSprites
from support import *
from timer import Timer
from random import randint

class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.title = pygame.display.set_caption('Platformer')
        self.clock = pygame.time.Clock()
        self.running = True

        #groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()


        #load game
        self.load_assets()
        self.setup()

        #timers
        self.bee_timer = Timer(500,func = self.create_bee,repeat = True,autoStart = True)
    
    def create_bee(self):
        Bee((randint(300,600),randint(300,600)),self.bee_frames,self.all_sprites)

    def create_bullet(self,pos,direction):
        self.audio['shoot'].play()
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet((x,pos[1]),self.bullet_surf,direction,(self.all_sprites,self.bullet_sprites))
        Fire(pos,self.fire_surf,self.player,self.all_sprites)


    def load_assets(self):
        #graphics
        self.player_frames = import_folder('images','player')
        self.bullet_surf = import_image('images','gun','bullet')
        self.fire_surf = import_image('images','gun','fire')
        self.bee_frames = import_folder('images','enemies','bee')
        self.worm_frames = import_folder('images','enemies','worm')

        #audio
        self.audio = import_sound('audio')
        self.audio['music'].play()

    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))
        for x,y,image in map.get_layer_by_name('Main').tiles():
            Sprites((x * TILE_SIZE, y * TILE_SIZE),image,(self.all_sprites,self.collision_sprites))
        
        for x,y,image in map.get_layer_by_name('Decoration').tiles():
            Sprites((x * TILE_SIZE,y * TILE_SIZE),image,self.all_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y),self.player_frames,self.collision_sprites,self.create_bullet,self.all_sprites)
            if obj.name == 'Worm':
                Worm((obj.x,obj.y),self.worm_frames,self.all_sprites)

    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            #update
            self.bee_timer.update()
            self.all_sprites.update(dt)

            #draw
            self.display_surface.fill(BG_COLOGR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
