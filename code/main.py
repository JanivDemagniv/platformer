from setteing import *
from sprites import *
from groups import AllSprites
from support import *

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


        #load game
        self.load_assets()
        self.setup()

    def load_assets(self):
        self.player_frames = import_folder('images','player')
        self.bullet_surf = import_image('images','gun','bullet')
        self.fire_surf = import_image('images','gun','fire')
        self.bee_frames = import_folder('images','enemies','bee')
        self.worm_frames = import_folder('images','enemies','worm')
        self.background_music = import_sound('audio','music')

    def setup(self):
        map = load_pygame(join('data','maps','world.tmx'))
        for x,y,image in map.get_layer_by_name('Main').tiles():
            Sprites((x * TILE_SIZE, y * TILE_SIZE),image,(self.all_sprites,self.collision_sprites))
        
        for x,y,image in map.get_layer_by_name('Decoration').tiles():
            Sprites((x * TILE_SIZE,y * TILE_SIZE),image,self.all_sprites)

        for obj in map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x,obj.y),self.player_frames,self.collision_sprites,self.all_sprites)
            if obj.name == 'Bee':
                Bee((obj.x,obj.y),self.bee_frames,self.all_sprites)
            if obj.name == 'Worm':
                Worm((obj.x,obj.y),self.worm_frames,self.all_sprites)

    def run(self):
        self.background_music.play()
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            #update
            self.all_sprites.update(dt)

            #draw
            self.display_surface.fill(BG_COLOGR)
            self.all_sprites.draw(self.player.rect.center)
            pygame.display.update()
        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
