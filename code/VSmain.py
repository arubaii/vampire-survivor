from VSsetup import *
from VSsettings import *
from VSassets import *
from VSsprites import *
from VSplayer import Player
from VSgroups import AllSprites
from random import randint

class Game:
    def __init__(self):


        self.display = initialize() 
        self.clock = pg.Clock()
        self.running = True

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()
        self.enemy_sprites = pg.sprite.Group()

        self.enemy_spawn_positions = []                   # Enemy spawn positions
        self.start_pos = load_assets(self)
        print(self.player_up)
        # Class instances
        self.player = Player(self.start_pos, self.player_left, self.player_right,
                             self.player_up, self.player_down, self.all_sprites, 
                             self.collision_sprites) 
        self.bullet = Gun(self.player, self.shoot_sound, self.bullet_sprites, self.all_sprites)
        self.kill_count = 0

        self.enemy_event = pg.event.custom_type()
        pg.time.set_timer(self.enemy_event, 300)

        # Audio setup
        self.shoot_sound.set_volume(0.4)
        self.impact_sound.set_volume(0.4)
        self.music.set_volume(0.05)                 # Could be its own 'play_music' func to turn off and on
        self.music.play()
        self.music.play(loops=-1)

        self.setup()

    def bullet_collision(self):
        # Checks if we have shot a bullet
        for bullet in self.bullet_sprites:
            collision_sprites = pg.sprite.spritecollide(bullet, self.enemy_sprites, False, pg.sprite.collide_mask)
            if collision_sprites:
                for sprite in collision_sprites:
                    # Enemy and bullet destruction
                    sprite.destroy()
                    self.impact_sound.play()
                    self.kill_count += 1
                    bullet.kill()

    def setup(self):
        ground(self)
        objects(self) 
        collision(self)  
    

    def run(self):
        while self.running:
            # How much time passes each frame
            dt = self.clock.tick(FPS) / 1000
            
            for event in pg.event.get():
                # Or Alt + f4 on Windows, Cmd + Q on MacOS
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.running = False
                if event.type == self.enemy_event:
                    self.enemy = Enemies(self.player, self.bat, self.blob, self.skeleton,
                                         choice(self.enemy_spawn_positions), self.collision_sprites, 
                                         self.bullet_sprites, self.all_sprites, self.enemy_sprites)


            self.all_sprites.update(dt)
            self.bullet_collision()

            # Game draw
            self.display.fill(BACKGROUND_COLOR)
            self.all_sprites.draw(self.player.rect.center)

            fps_counter(self.display, self.clock, FPS_TOGGLE)
            kill_text(self.display, self.kill_count)
            pg.display.flip()
            
    pg.quit()


# Game instance
if __name__ == '__main__':
    game = Game()
    game.run()

