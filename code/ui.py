import pygame

class UI:
    def __init__(self, game):
        self.game = game  
        self.bar_width = 200  
        self.bar_height = 20 
        self.player_bar_pos = (50, 50)  
        self.enemy_bar_pos = (self.game.display_surface.get_width() - 250, 50) 

        self.bg_color = (0, 0, 0)  
        self.health_color = (255, 0, 0)  
        self.border_color = (255, 255, 255)  

    def draw_health_bar(self, health, max_health, position):
        x, y = position
        pygame.draw.rect(self.game.display_surface, self.bg_color, (x, y, self.bar_width, self.bar_height))
        health_width = int(self.bar_width * (health / max_health))
        pygame.draw.rect(self.game.display_surface, self.health_color, (x, y, health_width, self.bar_height))
        pygame.draw.rect(self.game.display_surface, self.border_color, (x, y, self.bar_width, self.bar_height), 3)

    def draw(self):
        self.draw_health_bar(self.game.player.health, self.game.player.max_health, self.player_bar_pos)
        for enemy in self.game.enemy_sprites:
            if enemy.health > 0:
                self.draw_health_bar(enemy.health, enemy.max_health, self.enemy_bar_pos)