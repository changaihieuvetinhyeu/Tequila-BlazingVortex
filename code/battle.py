import pygame
import random
from settings import *

class Creature:
    def __init__(self, name, health, mana, x, y):
        self.name = name
        self.health = health
        self.mana = mana
        self.max_health = health
        self.max_mana = mana
        self.x = x  # Tọa độ của nhân vật
        self.y = y
        self.alive = True

    def take_damage(self, damage):
        """Nhận sát thương từ đối thủ"""
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def heal(self):
        """Hồi máu"""
        if self.mana >= 2:
            self.health += 20
            if self.health > self.max_health:
                self.health = self.max_health
            self.mana -= 2
            return True
        return False

    def attack(self, target):
        """Tấn công đối thủ"""
        if self.mana >= 1:
            damage = 15
            target.take_damage(damage)
            self.mana -= 1
            return True
        return False

    def is_alive(self):
        """Kiểm tra xem Creature có còn sống không"""
        return self.alive

    def reset(self):
        """Reset lại trạng thái ban đầu"""
        self.health = self.max_health
        self.mana = self.max_mana
        self.alive = True

class Battle:
    def __init__(self, player, opponent, display_surface):
        self.player = player
        self.opponent = opponent
        self.display_surface = display_surface
        self.font = pygame.font.Font(None, 36)

    def player_turn(self, action):
        """Xử lý lượt của người chơi"""
        if action == 'attack':
            if self.player.attack(self.opponent):
                print(f"{self.player.name} tấn công!")
                # Hiệu ứng tấn công
                self.show_attack_effect(self.opponent.x, self.opponent.y)
        elif action == 'heal':
            if self.player.heal():
                print(f"{self.player.name} hồi máu!")
                # Hiệu ứng hồi máu
                self.show_heal_effect(self.player.x, self.player.y)

    def opponent_turn(self):
        """Xử lý lượt của đối thủ AI"""
        action = random.choice(['attack', 'heal'])
        if action == 'attack':
            if self.opponent.attack(self.player):
                print(f"{self.opponent.name} tấn công!")
                self.show_attack_effect(self.player.x, self.player.y)
        elif action == 'heal':
            if self.opponent.heal():
                print(f"{self.opponent.name} hồi máu!")
                self.show_heal_effect(self.opponent.x, self.opponent.y)

    def show_attack_effect(self, x, y):
        """Hiển thị hiệu ứng tấn công (lửa)"""
        # Bạn có thể sử dụng các hình ảnh và âm thanh ở đây
        fire_image = pygame.image.load('Tequila-BlazerVortex-main/images/fighting/fire.png')
        fire_rect = fire_image.get_rect(center=(x, y))
        self.display_surface.blit(fire_image, fire_rect)
        pygame.display.update()

    def show_heal_effect(self, x, y):
        """Hiển thị hiệu ứng hồi máu"""
        heal_image = pygame.image.load('Tequila-BlazerVortex-main/images/fighting/green.png')
        heal_rect = heal_image.get_rect(center=(x, y))
        self.display_surface.blit(heal_image, heal_rect)
        pygame.display.update()

    def update_ui(self):
        """Cập nhật UI (hiển thị HP và Mana)"""
        player_health_text = self.font.render(f"HP: {self.player.health}/{self.player.max_health}", True, (255, 255, 255))
        player_mana_text = self.font.render(f"Mana: {self.player.mana}/{self.player.max_mana}", True, (255, 255, 255))
        opponent_health_text = self.font.render(f"HP: {self.opponent.health}/{self.opponent.max_health}", True, (255, 255, 255))
        opponent_mana_text = self.font.render(f"Mana: {self.opponent.mana}/{self.opponent.max_mana}", True, (255, 255, 255))

        self.display_surface.blit(player_health_text, (20, 20))
        self.display_surface.blit(player_mana_text, (20, 60))
        self.display_surface.blit(opponent_health_text, (WINDOW_WIDTH - 200, 20))
        self.display_surface.blit(opponent_mana_text, (WINDOW_WIDTH - 200, 60))

        pygame.display.update()

    def is_game_over(self):
        """Kiểm tra kết thúc game"""
        if not self.player.is_alive():
            return "Player lost!"
        if not self.opponent.is_alive():
            return "Player won!"
        return None
