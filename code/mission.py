import pygame
from settings import *
from ui import UI

class Mission:
    def __init__(self, game, dialogue, on_complete=None, fill_screen=False,sound_file = None):
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
        self.speaker_name = None  
        self.full_text = ""  
        self.guide_active = False
        self.guide_timer = 0
        self.guide_duration = 5000  
        self.guide_x = self.game.display_surface.get_width()  

        self.sound_file = sound_file
        self.tint_sound = None
        if self.sound_file:
            self.tint_sound = pygame.mixer.Sound(self.sound_file)
            self.tint_sound.play()
            self.tint_sound.set_volume(0.75)
        else:
            self.tint_sound = None

    def draw_dialogue_box(self):
        box_width = self.game.display_surface.get_width() * 0.9
        box_height = self.game.display_surface.get_height() * 0.25
        box_x = (self.game.display_surface.get_width() - box_width) / 2
        box_y = self.game.display_surface.get_height() - box_height - 20

        dialogue_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        dialogue_surface.fill((0, 0, 0, 0))  

        pygame.draw.rect(dialogue_surface, (192, 192, 192, 180), (0, 0, box_width, box_height), border_radius=20)

        # Vẽ viền trắng xung quanh
        pygame.draw.rect(dialogue_surface, WHITE, (0, 0, box_width, box_height), width=4, border_radius=20)

        # Vẽ hộp thoại lên màn hình
        self.game.display_surface.blit(dialogue_surface, (box_x, box_y))

        return box_x, box_y

    def draw_speaker_box(self, speaker_name, box_x, box_y):
        font = pygame.font.Font('data/fonts/FVF Fernando 08.ttf', 28)
        text_surface = font.render(speaker_name, True, WHITE)  
        text_width = text_surface.get_width()
        text_height = font.size("T")[1]

        box_width = text_width + 20  
        box_height = text_height + 10

        
        box_y = box_y - box_height - 5

        speaker_surface = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        speaker_surface.fill((0, 0, 0, 0))  

        pygame.draw.rect(speaker_surface, (192, 192, 192, 180), (0, 0, box_width, box_height), border_radius=15)

        pygame.draw.rect(speaker_surface, WHITE, (0, 0, box_width, box_height), width=3, border_radius=15)

        self.game.display_surface.blit(speaker_surface, (box_x, box_y))

        text_x = box_x + 10
        text_y = box_y + (box_height - text_height) / 2
        self.game.display_surface.blit(text_surface, (text_x, text_y))

    def show_dialog(self):
        if not self.running:
            return
        
        if self.dialog_index < len(self.dialogue):
            current_dialogue = self.dialogue[self.dialog_index]

            if ":" in current_dialogue:
                self.speaker_name, self.full_text = current_dialogue.split(":", 1)
            else:
                self.speaker_name = None
                self.full_text = current_dialogue

            current_time = pygame.time.get_ticks()
            if current_time - self.last_typing_time > self.typing_speed and len(self.typed_text) < len(self.full_text):
                self.typed_text += self.full_text[len(self.typed_text)]
                self.last_typing_time = current_time
        else:
            self.running = False  

        box_x, box_y = self.draw_dialogue_box()
        box_width = self.game.display_surface.get_width() * 0.9  
        box_height = self.game.display_surface.get_height() * 0.25

        tip_font = pygame.font.Font('data/fonts/FVF Fernando 08.ttf', 24)
        tip_text = tip_font.render("Nhấn SPACE để bỏ qua", True, WHITE)
        tip_x = box_x + box_width - tip_text.get_width() - 20
        tip_y = box_y + box_height - tip_text.get_height() - 15  
        self.game.display_surface.blit(tip_text, (tip_x, tip_y))

        if self.speaker_name:
            self.draw_speaker_box(self.speaker_name.strip(), box_x, box_y)

        font = pygame.font.Font('data/fonts/FVF Fernando 08.ttf', 32)
        box_width -= 40  

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
            text_surface = font.render(line, True, WHITE)
            self.game.display_surface.blit(text_surface, (box_x + 20, box_y + 15 + i * line_height))

        

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

        line_height = font.size("T")[1] + 10
        total_height = len(lines) * line_height
        start_y = (self.game.display_surface.get_height() - total_height) / 2

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, WHITE)
            text_width = text_surface.get_width()
            x = (self.game.display_surface.get_width() - text_width) / 2
            y = start_y + i * line_height
            self.game.display_surface.blit(text_surface, (x, y))

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.typed_text = full_text


    def handle_input(self):
        if not self.running:
            return

        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] and current_time - self.last_space_press > self.space_cooldown:
            self.last_space_press = current_time  

            if len(self.typed_text) < len(self.full_text):
                self.typed_text = self.full_text
            else:
                self.dialog_index += 1
                if self.dialog_index >= len(self.dialogue):
                    self.running = False
                else:
                    self.speaker_name, self.full_text = (self.dialogue[self.dialog_index].split(":", 1) if ":" in self.dialogue[self.dialog_index] else (None, self.dialogue[self.dialog_index]))
                    self.typed_text = ""

    def update(self):
        if self.fill_screen:
            self.game.display_surface.fill(BLACK)
        self.handle_input()
        self.show_dialog()

        if not self.running and self.guide_active:
            self.game.show_guide(self.game.clock.get_time() / 1000)  

        if not self.running and self.on_complete and not self.guide_active:
            self.on_complete()  
            self.on_complete = None
