from VSsetup import DISPLAY_WIDTH, DISPLAY_HEIGHT, DEBUG, TILE_SIZE
from VSsettings import *
from VSassets import *
from math import atan2, degrees
import random
from random import randint, choice


class Sprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)
        self.ground = True

class CollisionSprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(topleft = pos)


class TransparentSprite(pg.sprite.Sprite):
    def __init__(self, pos, length, width, groups, RGB, debug):
        super().__init__(groups)
        self.image = pg.Surface((length, width), pg.SRCALPHA)
        # Transparent fill for debugging, otherwise set alpha to 0
        self.debug = debug
        if self.debug:
            self.image.fill((RGB))
            self.image.set_alpha(100) 
        self.rect = self.image.get_frect(topleft = pos)


class Gun(pg.sprite.Sprite):
    def __init__(self, player, shoot_sound, bullet_sprites, *groups):
        # Player connection
        self.player = player
        self.distance = 140 * 0.75
        self.player_direction = pg.Vector2(0,1)
        # Sprite setup
        super().__init__(*groups)
        self.gun_surf = IMAGE_PATHS["gun"].convert_alpha()
        self.gun_surf = pg.transform.rotozoom(self.gun_surf, angle=0, scale=0.75)
        self.image = self.gun_surf
        self.bullet = None
        # Positions the gun away from the center of the player, by the position vector * distance
        self.rect = self.image.get_frect(center = self.player.rect.center + self.player_direction * self.distance)


        # Bullet attributes
        self.can_shoot = True
        self.gun_shoot_time = 0
        self.cooldown_duration = 400

        self.shoot_sound = shoot_sound
        self.all_sprites = groups
        self.bullet_sprites = bullet_sprites

    def get_direction(self):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        player_pos = pg.Vector2(DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        # The position of the mouse relative to the player's position for a vector range -1 to 1
        self.player_direction = (mouse_pos - player_pos).normalize()
    
    def rotate_gun(self):
        '''
        The math:

        To find the angle from the player to gun, we must find the arctangent angle which is simple here, given
        a triangle that forms from the center of the player, to the center of the gun. We then use the opposite side
        divided by the adjacent side (theta = arctan(opp/ adj)) to find the angle at each frame. Finally we subtract 90 from the 
        operation so that the oreintation of the angle always points outwards, instead of rotating in a circular motion. 
        '''
        angle_theta = degrees(atan2(self.player_direction.x, self.player_direction.y)) - 90
        if self.player_direction.x > 0:
            self.image = pg.transform.rotozoom(self.gun_surf, angle_theta, 1)
        else:
            self.image = pg.transform.rotozoom(self.gun_surf, abs(angle_theta), 1)
            self.image = pg.transform.flip(self.image, False, True)

    def update(self, _):
        self.get_direction()
        self.rotate_gun()
        # The position of the gun updates every frame as the game moves
        self.rect.center = self.player.rect.center + self.player_direction * self.distance

        mouse_press = pg.mouse.get_just_pressed()
        if mouse_press[0] and self.can_shoot:
            
            self.bullet_speed = 1500 
            # Multiply the positional vector by 50 so that the bullet appears to shoot out the gun
            self.bullet_pos = self.rect.center + self.player_direction * 50
            self.bullet = Bullet(self.bullet_pos, self.player_direction, self.bullet_speed, 
                                 self.all_sprites, self.bullet_sprites)
            self.can_shoot = False
            self.gun_shoot_time = pg.time.get_ticks()
            self.shoot_sound.play()
        self.bullet_timer()
        


    def bullet_timer(self):
        if not self.can_shoot:
            current_time = pg.time.get_ticks()
            # If enough time has passed since user has shot a laser, they may fire again
            if current_time - self.gun_shoot_time > self.cooldown_duration:
                self.can_shoot = True

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, player_direction, bullet_speed, *groups):
        super().__init__(*groups)
        self.image = IMAGE_PATHS['bullet'].convert_alpha()
        self.image = pg.transform.rotozoom(self.image, angle=0, scale=0.75)
        self.rect = self.image.get_frect(center = pos)
        self.player_direction = player_direction
        self.bullet_speed = bullet_speed
        
        self.spawn_time = pg.time.get_ticks()
        self.lifetime = 1000


    def update(self, dt):
        self.rect.center += self.player_direction * self.bullet_speed * dt
        if pg.time.get_ticks() - self.spawn_time >= self.lifetime:
            self.kill()

        

class Enemies(pg.sprite.Sprite):
    def __init__(self, player: list, bat: list, blob: list, skeleton: list, spawn_positions: list, collsion_sprites, bullet_sprites, *groups):
        super().__init__(*groups)

        self.player = player
        self.all_sprites, self.enemy_sprites = groups
        self.collision_sprites = collsion_sprites
        self.bullet_sprites = bullet_sprites

        self.animations = {
        "bat": bat,
        "blob": blob, 
        "skeleton": skeleton   
        }
        
        self.enemy = choice(["bat", "blob", "skeleton"])
        self.frames = self.animations[self.enemy]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_frect(center=(spawn_positions))
        self.rect_hitbox = self.rect.inflate(-20, -40)

        # Enemy attributes
        self.enemy_speed = 100 # change later with if statements for each enemy
        self.animation_speed = 4

        self.death_time = 0
        self.death_duration = 400

    def movement_track(self, dt):
        ''''Handles mob tracking logic'''
        self.enemy_pos = pg.Vector2(self.rect.center)
        self.player_pos = pg.Vector2(self.player.rect.center)
        self.direction = (self.player_pos - self.enemy_pos).normalize()
        
        self.rect_hitbox.x += self.enemy_speed * self.direction.x * dt
        self.collsion('horizontal')
        self.rect_hitbox.y += self.enemy_speed * self.direction.y * dt
        self.collsion('vertical')
        
        self.rect.center = self.rect_hitbox.center

    def death_timer(self):
        if pg.time.get_ticks() - self.death_time >= self.death_duration:
            self.kill()

    def destroy(self):
        self.death_time = pg.time.get_ticks()

        surf = pg.mask.from_surface(self.frames[0]).to_surface()
        surf.set_colorkey('black')
        self.image = surf

    def collsion(self,direction):
        '''Handles all of object collision logic'''
        # Iterate over all collision sprites each frame to check for collisions
        for sprite in self.collision_sprites:
            # Returns True if any part of the two rects overlap (player and object), including edges
            # However, it does NOT determine which side the collision occurs on—only that an overlap exists
            if sprite.rect.colliderect(self.rect_hitbox):
                if direction == 'horizontal':
                     # If the player is moving right (positive velocity), snap their right side to the object's left side
                    if self.direction.x > 0: self.rect_hitbox.right = sprite.rect.left
                    # And vice-versa
                    if self.direction.x < 0: self.rect_hitbox.left = sprite.rect.right
                else: # Vertical collision
                     # If the player is moving up (negative velocity), snap their top side to the object's bottom side
                    if self.direction.y < 0: self.rect_hitbox.top = sprite.rect.bottom
                    # and vice-versa
                    if self.direction.y > 0: self.rect_hitbox.bottom = sprite.rect.top
        
    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        # Update image to match current frame
        self.image = self.frames[int(self.frame_index) % len(self.frames)]


    def update(self, dt):
        if self.death_time == 0:
            self.movement_track(dt)
            self.animate(dt)

        else:                  
            # If the death timer has started, the enemy sprite no longer moves or animates 
            self.death_timer()




# LOADING SPRITE ASSETS ___________________________________________________________________________________________________________________________________________________________________________________________________________

def ground(self):
    for x,y, image in self.map.get_layer_by_name('Ground').tiles():
        Sprite((x * TILE_SIZE ,y * TILE_SIZE ), image, self.all_sprites)

def objects(self):
    for obj in self.map.get_layer_by_name('Objects'):
        CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
        # RGB value for debugging, otherwise set (0,0,0)
        if DEBUG:
            TransparentSprite((obj.x, obj.y), obj.width, obj.height, (self.all_sprites, self.collision_sprites), RGB=(0,0,255), debug=DEBUG)

def collision(self):
    for col in self.map.get_layer_by_name('Collisions'):
        TransparentSprite((col.x, col.y), col.width, col.height, (self.all_sprites, self.collision_sprites), RGB=(255,0,0), debug=DEBUG)


