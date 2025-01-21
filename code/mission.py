import pygame
from settings import *
from ui import UI

class Mission:
    def __init__(self, game, dialogue, on_complete=None, fill_screen=False):
        self.game = game
        self.dialogue = dialogue
        self.dialog_index = 0
        self.typed_text = ""
        self.typing_speed = 50  
        self.last_typing_time = 0
        self.running = True
        self.fill_screen = fill_screen
        self.on_complete = on_complete
        self.last_space_press = 0  
        self.space_cooldown = 200  

    def draw_dialogue_box(self):
        box_width = self.game.display_surface.get_width() * 0.9
        box_height = self.game.display_surface.get_height() * 0.2
        box_x = (self.game.display_surface.get_width() - box_width) / 2
        box_y = self.game.display_surface.get_height() - box_height - 20

        pygame.draw.rect(self.game.display_surface, (0, 0, 0), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(self.game.display_surface, (255, 255, 255), (box_x, box_y, box_width, box_height), 3)

        return box_x, box_y

    def show_dialog(self):
        if not self.running:
            return

        if self.dialog_index < len(self.dialogue):
            full_text = self.dialogue[self.dialog_index]
            current_time = pygame.time.get_ticks()
            if current_time - self.last_typing_time > self.typing_speed and len(self.typed_text) < len(full_text):
                self.typed_text += full_text[len(self.typed_text)]
                self.last_typing_time = current_time
        else:
            self.running = False  

        font = pygame.font.Font('data/fonts/SVN-Retron 2000.otf', 34)
        box_x, box_y = self.draw_dialogue_box()
        box_width = self.game.display_surface.get_width() * 0.9 - 40  

        words = self.typed_text.split()
        lines = []
        current_line = ""

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= box_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        line_height = font.size("T")[1] + 5
        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            self.game.display_surface.blit(text_surface, (box_x + 20, box_y + 20 + i * line_height))

    def show_centered_text(self):
        if not self.running:
            return

        if self.dialog_index < len(self.dialogue):
            full_text = self.dialogue[self.dialog_index]
            current_time = pygame.time.get_ticks()
            if current_time - self.last_typing_time > self.typing_speed and len(self.typed_text) < len(full_text):
                self.typed_text += full_text[len(self.typed_text)]
                self.last_typing_time = current_time
        else:
            self.running = False

        font = pygame.font.Font('data/fonts/SVN-Retron 2000.otf', 48)

        # Chia văn bản thành các dòng phù hợp
        words = self.typed_text.split()
        lines = []
        current_line = ""
        max_width = self.game.display_surface.get_width() * 0.8

        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Tính toán để căn giữa toàn bộ đoạn text
        line_height = font.size("T")[1] + 10
        total_height = len(lines) * line_height
        start_y = (self.game.display_surface.get_height() - total_height) / 2

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            text_width = text_surface.get_width()
            x = (self.game.display_surface.get_width() - text_width) / 2
            y = start_y + i * line_height
            self.game.display_surface.blit(text_surface, (x, y))


    def handle_input(self):
        if not self.running:
            return

        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and current_time - self.last_space_press > self.space_cooldown:
            self.last_space_press = current_time  

            if len(self.typed_text) < len(self.dialogue[self.dialog_index]):
                self.typed_text = self.dialogue[self.dialog_index]
            else:
                self.dialog_index += 1
                if self.dialog_index >= len(self.dialogue):
                    self.running = False
                else:
                    self.typed_text = ""

    def update(self):
        if self.fill_screen:
            self.game.display_surface.fill(BLACK)
        self.handle_input()
        self.show_dialog()

        if not self.running and self.on_complete:
            self.on_complete()  
            self.on_complete = None  
