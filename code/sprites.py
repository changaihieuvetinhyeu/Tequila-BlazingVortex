from settings import * 
from math import atan2, degrees
import pygame

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.ground = True

class CollisionSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, player, collision_sprites):
        super().__init__(groups)
        self.player = player
        self.blocked = False
        self.defeated = False

        self.frames = frames
        self.frame_index = 0
        self.original_image = self.frames[self.frame_index]
        self.image = self.original_image.copy()
        self.animation_speed = 6

        self.rect = self.image.get_rect(center=pos)
        self.hitbox_rect = self.rect.inflate(-20, -40)
        self.collision_sprites = collision_sprites
        self.direction = pygame.Vector2()
        self.speed = 200

        self.health = 50 
        self.max_health = 50  

        self.hit_time = 0
        self.hit_duration = 100  
        self.is_hit = False

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.frame_index %= len(self.frames)  
        self.original_image = self.frames[int(self.frame_index)]

    def move(self, dt):
        if self.blocked or self.defeated:
            return

        player_pos = pygame.Vector2(self.player.rect.center)
        enemy_pos = pygame.Vector2(self.rect.center)
        direction = player_pos - enemy_pos

        if direction.length() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.Vector2()

        self.hitbox_rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')
        self.hitbox_rect.y += self.direction.y * self.speed * dt
        self.collision('vertical')
        self.rect.center = self.hitbox_rect.center

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.hitbox_rect):
                if direction == 'horizontal':
                    if self.direction.x > 0:
                        self.hitbox_rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.hitbox_rect.left = sprite.rect.right
                elif direction == 'vertical':
                    if self.direction.y > 0:
                        self.hitbox_rect.bottom = sprite.rect.top
                    if self.direction.y < 0:
                        self.hitbox_rect.top = sprite.rect.bottom

    def block(self):
        self.blocked = True

    def unblock(self):
        self.blocked = False

    def take_damage(self, damage):
        if not self.defeated:
            self.health -= damage
            self.is_hit = True
            self.hit_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.kill()
                self.defeated = True
                self.block()  

    def update(self, dt):
        current_time = pygame.time.get_ticks()

        if self.is_hit:
            self.image = self.original_image.copy()
            white_surf = pygame.Surface(self.image.get_size(), flags=pygame.SRCALPHA)
            white_surf.fill((255, 255, 255, 128))
            self.image.blit(white_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            if current_time - self.hit_time > self.hit_duration:
                self.is_hit = False

        elif not self.defeated:
            
            self.image = self.original_image.copy()

        if not self.defeated:
            self.move(dt)
            self.animate(dt)


