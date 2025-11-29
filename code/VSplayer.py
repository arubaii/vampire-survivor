from VSsettings import *
from VSassets import *
from VSsprites import *

'''Handles all the controls and movement logic for the palyer'''
class Player(pg.sprite.Sprite):
    def __init__(self, start_pos, left, right, up, down, groups, collsion_sprites):
        super().__init__(groups)
        
        # Store animations
        self.animations = {
            "left": left,
            "right": right,
            "up": up,
            "down": down
        }
        
        self.start_pos = start_pos
        # Default animation states
        self.current_animation = "down"
        self.frames = self.animations[self.current_animation]
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_frect(center=(self.start_pos))
        self.rect_hitbox = self.rect.inflate(-60, -90)

        # Movement attributes
        self.player_pos = pg.Vector2()
        self.player_speed = 500
        self.animation_speed = 4  # FPS
        self.collision_sprites = collsion_sprites

    def input(self):
        self.keys = pg.key.get_pressed()
        # Movement vector
        self.player_pos.x = int(self.keys[pg.K_d]) - int(self.keys[pg.K_a]) # Both are return boolean values
        self.player_pos.y = int(self.keys[pg.K_s]) - int(self.keys[pg.K_w])
    

    
    def movement(self, dt):
        self.input()
        # Update animation state
        if self.keys[pg.K_w]:
            self.current_animation = "up"
        elif self.keys[pg.K_s]:
            self.current_animation = "down"
        elif self.keys[pg.K_a]:
            self.current_animation = "left"
        elif self.keys[pg.K_d]:
            self.current_animation = "right"
        
        # Moving the player
        self.rect_hitbox.x += self.player_pos.x * self.player_speed * dt 
        self.collision('horizontal')
        self.rect_hitbox.y += self.player_pos.y * self.player_speed * dt   
        self.collision('vertical')

        self.rect.center = self.rect_hitbox.center
        
    def collision(self, direction):
        '''Handles all of object collision logic'''

        # Iterate over all collision sprites each frame to check for collisions
        for sprite in self.collision_sprites:

            # Returns True if any part of the two rects overlap (player and object), including edges
            # However, it does NOT determine which side the collision occurs on—only that an overlap exists
            if sprite.rect.colliderect(self.rect_hitbox):
                if direction == 'horizontal':
                     # If the player is moving right (positive velocity), snap their right side to the object's left side
                    if self.player_pos.x >= 0: self.rect_hitbox.right = sprite.rect.left
                    # And vice-versa
                    if self.player_pos.x <= 0: self.rect_hitbox.left = sprite.rect.right
                else: # Vertical collision
                     # If the player is moving up (negative velocity), snap their top side to the object's bottom side
                    if self.player_pos.y <= 0: self.rect_hitbox.top = sprite.rect.bottom
                    # and vice-versa
                    if self.player_pos.y >= 0: self.rect_hitbox.bottom = sprite.rect.top

    def update(self, dt):
        '''Handles animation updates'''
    
        self.movement(dt)

        # Normalize the player velocity vector for diagonal movement
        if self.player_pos.length() > 0:
            self.player_pos = self.player_pos.normalize()
        # No animation state if the player is not moving
        else:
            self.frame_index = 0


        # Set frames based on current movement

        # Handle frame animation
        self.frame_index += self.animation_speed * dt
        self.frame_index %= len(self.frames)  # Ensure looping

        # Update image to match current frame
        self.image = self.frames[int(self.frame_index)]

        # Grab player rect position for enemy tracking
        return self.rect


        

 

