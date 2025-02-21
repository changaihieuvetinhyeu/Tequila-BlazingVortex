import pygame
from battle import *
import json
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from mission import Mission
from intro import intro_screen, pause_screen
from battle import *

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Blazing Vortex")
        self.clock = pygame.time.Clock()
        self.running = True
        self.dialogues = self.load_dialogues()
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.show_timer = False
        self.finished = False
        self.dialogue = None
        self.timer = 60
        self.fill = False
        self.guide_active = False
        self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 255
        self.tint_direction = -1
        self.tint_speed = 600
        self.show_choice = False
        self.show_ui = False
        self.map = None
        self.player = None
        self.achievement_active = False

        self.guide_x = self.display_surface.get_width()

        self.achievement_message = ""
        self.achievement_duration = 5000  # Thời gian hiển thị thành tựu (5 giây)
        self.achievement_speed = 600  # Tốc độ thụt vào của thông báo
        self.achievement_x = self.display_surface.get_width()
        
    def load_dialogues(self):
        with open('Tequila-BlazerVortex-main/code/dialogues.json', 'r', encoding='utf-8') as f:
            return json.load(f)

    def clear_sprites(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.enemy_sprites.empty()

    def setup(self, map_name):
        map = load_pygame(join('Tequila-BlazerVortex-main', 'data', 'maps', map_name))
        self.map = map
        ground_layer = map.get_layer_by_name("Ground")
        if ground_layer:
            for x, y, image in ground_layer.tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        entities_layer = map.get_layer_by_name("Entities")
        if entities_layer:
            for obj in entities_layer:
                if obj.name == "Player":
                    self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)

    def first_one_dialog(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/controversy.jpeg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["first_one_dialog"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.mini_game_two)
        )


    def first_two_dialog(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/fight1.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["first_two_dialog"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.second_one_dialogue)
        )

    def second_one_dialogue(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/defeat1.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["second_one_dialogue"],
            fill_screen=False,
            sound_file='Tequila-BlazerVortex-main/sound/punch.mp3',
            on_complete=lambda: self.transition(self.second_two_dialogue)
        )

    def second_two_dialogue(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/wakinup.jpeg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["second_two_dialogue"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.second_mission)
        )

    def second_mission(self):
        self.clear_sprites()
        self.show_ui = False
        self.setup('first.tmx')
        self.start_timer()
        self.finished = True

    def start_timer(self):
        self.fill = True
        self.dialogue = None
        self.guide_active = True
        self.guide_timer = pygame.time.get_ticks()
        self.show_timer = True
        self.timer = 5

    def third_mission(self):
        self.clear_sprites()
        self.show_timer = False
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, -100))
        self.dialogue = Mission(
            self,
            self.dialogues["third_mission"],
            sound_file=None,
            on_complete=lambda: self.transition(self.choice)
        )

    def bad_ending(self):
        self.show_choice = False
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["bad_ending"],
            fill_screen=True,
            sound_file=None,
            on_complete=lambda: self.transition(self.consequence_one)
        )
    
    def consequence_one(self):
        self.show_choice = False
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/BE2.png').convert()
        self.dialogue = Mission(
            self,
            self.dialogues["consequence_one"],
            fill_screen=True,
            sound_file=None,
            on_complete=lambda: self.transition(self.restart_game)
        )

    def choice(self):
        self.show_choice = True

    def fourth_mission(self):
        self.show_choice = False
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["fourth_mission"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.moving_screen_one)
        )
    
    def moving_screen_one(self):
        self.fill = True
        self.dialogue = Mission(
            self,
            [
                "Mấy ngày hôm sau"
            ],
            fill_screen = True,
            on_complete=lambda: self.transition(self.fifth_mission)
        )
        self.dialogue.show_dialog = self.dialogue.show_centered_text

    def fifth_mission(self):
        self.show_choice = False
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/revenge3.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["fifth_mission"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.moving_screen_three)
        )

    def moving_screen_three(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/fight2.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_three"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.mini_game_two)
        )

    def mini_game_two(self):
        pass


    def moving_screen_four(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_four"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.moving_screen_five)
        )

    def moving_screen_five(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/bounded.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_five"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.moving_screen_six)
        )
    
    def moving_screen_six(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/revenge2.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_six"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.moving_screen_seven)
        )

    def moving_screen_seven(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/outburst.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_three"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.alternate)
        )
    
    def alternate(self):
        self.fill = True
        self.dialogue = Mission(
            self,
            [
                "Trong khi đó"
            ],
            fill_screen = True,
            on_complete=lambda: self.transition(self.moving_screen_eight)
        )
        self.dialogue.show_dialog = self.dialogue.show_centered_text

    def moving_screen_eight(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/wakinup2.png').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_eight"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.sixth_mission)
    )
        
    def sixth_mission(self):
        pass
        
    def moving_screen_nine(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_nine"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.moving_screen_ten)
        )

    def moving_screen_ten(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_ten"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.moving_screen_eleven)
        )

    def moving_screen_eleven(self):
        self.background = pygame.image.load('Tequila-BlazerVortex-main/images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            self.dialogues["moving_screen_nine"],
            fill_screen=False,
            sound_file=None,
            on_complete=lambda: self.transition(self.final_battle)
        )

    def final_battle(self):
        pass

    def good_ending(self):
        self.show_choice = False
        self.background = None
        self.dialogue = Mission(
            self,
            self.dialogues["good_ending"],
            fill_screen=True,
            sound_file=None,
            on_complete=lambda: self.transition(self.consequence_two)
        )
    
    def consequence_two(self):
        self.show_choice = False
        self.background = None
        self.dialogue = Mission(
            self,
            self.dialogues["consequence_two"],
            fill_screen=True,
            sound_file=None,
            on_complete=lambda: self.transition(self.restart_game)
        )

    def restart_game(self):
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.dialogue = None
        self.timer = 60
        self.fill = False
        self.tint_mode = 'untint'
        self.tint_progress = 255
        self.show_ui = False
        self.map = None
        self.player = None
        self.background = None
        intro_screen()
        self.first_one_dialog()

    def draw_timer(self):
        font = pygame.font.Font("Tequila-BlazerVortex-main/data/fonts/Font.ttf", 32)
        timer_text = font.render(f"Thời gian còn lại: {int(self.timer)}", True, WHITE)
        self.display_surface.blit(timer_text, (10, 10))

    def handle_choice_input(self, yes_button, no_button):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if yes_button.collidepoint(pygame.mouse.get_pos()):
                    self.transition(self.fourth_mission)
                elif no_button.collidepoint(pygame.mouse.get_pos()):
                    print("User chose: Không")
                    self.transition(self.bad_ending)

    def show_choice_ui(self, yes_button, no_button):
        question_font = pygame.font.Font('Tequila-BlazerVortex-main/data/fonts/Font.ttf', 32)
        question_text = question_font.render("Quyết định của bạn là gì?", True, WHITE)
        self.display_surface.blit(question_text, (WINDOW_WIDTH // 2 - question_text.get_width() // 2, WINDOW_HEIGHT // 2 - 100))

        button_font = pygame.font.Font('Tequila-BlazerVortex-main/data/fonts/Font.ttf', 28)
        yes_text = button_font.render("Có", True, WHITE)
        no_text = button_font.render("Không", True, WHITE)

        pygame.draw.rect(self.display_surface, BUTTON_COLOR, yes_button, border_radius=15)
        pygame.draw.rect(self.display_surface, BUTTON_COLOR, no_button, border_radius=15)

        self.display_surface.blit(yes_text, (yes_button.x + (yes_button.width - yes_text.get_width()) // 2, yes_button.y + (yes_button.height - yes_text.get_height()) // 2))
        self.display_surface.blit(no_text, (no_button.x + (no_button.width - no_text.get_width()) // 2, no_button.y + (no_button.height - no_text.get_height()) // 2))

        pygame.display.update()

    def unblock_player_after_dialogue(self):
        self.dialogue = None
        self.player.unblock()

    def transition(self, next_mission):
        self.tint_mode = 'tint'
        self.next_mission = next_mission
        self.mission_ready = False
        self.background = None

    def show_guide(self, dt):
        guide_text = [
            "Hướng dẫn", 
            "Sử dụng các phím W, A, S, D hoặc các phím mũi tên",
            "để di chuyển nhân vật",
            "Bấm ESC để tạm dừng"
        ]

        font = pygame.font.Font('Tequila-BlazerVortex-main/data/fonts/Font.ttf', 18)
        text_surfaces = [font.render(line, True, WHITE) for line in guide_text]
        max_line_width = max(surface.get_width() for surface in text_surfaces)
        total_height = sum(surface.get_height() for surface in text_surfaces) + (len(text_surfaces) - 1) * 5

        guide_width = max_line_width + 20
        guide_height = total_height + 20
        guide_y = 20

        guide_surface = pygame.Surface((guide_width, guide_height), pygame.SRCALPHA)
        guide_surface.fill((192, 192, 192, 180))
        pygame.draw.rect(guide_surface, WHITE, (0, 0, guide_width, guide_height), width=3, border_radius=10)

        y_offset = 10
        for surface in text_surfaces:
            text_x = (guide_width - surface.get_width()) / 2
            text_y = y_offset
            guide_surface.blit(surface, (text_x, text_y))
            y_offset += surface.get_height() + 5

        target_x = self.display_surface.get_width() - guide_width - 20
        if self.guide_active:
            if self.guide_x > target_x:
                self.guide_x = max(self.guide_x - 600 * dt, target_x)
            elif pygame.time.get_ticks() - self.guide_timer > 5000:
                self.guide_active = False
        else:
            if self.guide_x < self.display_surface.get_width():
                self.guide_x += 600 * dt

        self.display_surface.blit(guide_surface, (self.guide_x, guide_y))

    def show_achivement(self, dt):
        guide_text = [
            "Thành tựu đạt được",
            "Chào mừng đến với thế giới của chúng tôi"
        ]

        font = pygame.font.Font('Tequila-BlazerVortex-main/data/fonts/Font.ttf', 18)
        text_surfaces = [font.render(line, True, WHITE) for line in guide_text]
        max_line_width = max(surface.get_width() for surface in text_surfaces)
        total_height = sum(surface.get_height() for surface in text_surfaces) + (len(text_surfaces) - 1) * 5

        guide_width = max_line_width + 20
        guide_height = total_height + 20
        guide_y = 20

        guide_surface = pygame.Surface((guide_width, guide_height), pygame.SRCALPHA)
        guide_surface.fill((192, 192, 192, 180))
        pygame.draw.rect(guide_surface, WHITE, (0, 0, guide_width, guide_height), width=3, border_radius=10)

        y_offset = 10
        for surface in text_surfaces:
            text_x = (guide_width - surface.get_width()) / 2
            text_y = y_offset
            guide_surface.blit(surface, (text_x, text_y))
            y_offset += surface.get_height() + 5

        target_x = self.display_surface.get_width() - guide_width - 20
        if self.guide_active:
            if self.guide_x > target_x:
                self.guide_x = max(self.guide_x - 600 * dt, target_x)
            elif pygame.time.get_ticks() - self.guide_timer > 5000:
                self.guide_active = False
        else:
            if self.guide_x < self.display_surface.get_width():
                self.guide_x += 600 * dt

        self.display_surface.blit(guide_surface, (self.guide_x, guide_y))

    def tint_screen(self, dt):
        if self.tint_mode == 'untint':
            self.tint_progress = max(0, self.tint_progress - self.tint_speed * dt)
        elif self.tint_mode == 'tint':
            self.tint_progress = min(255, self.tint_progress + self.tint_speed * dt)
            if self.tint_progress == 128 and self.dialogue and self.dialogue.sound_file:
                if self.dialogue.tint_sound:
                    self.dialogue.tint_sound.play()

            if self.tint_progress >= 255:
                if hasattr(self, 'next_mission') and self.next_mission:
                    if not self.mission_ready:
                        self.next_mission()
                        self.next_mission = None
                self.tint_mode = 'untint'

        self.tint_surf.set_alpha(self.tint_progress)
        self.display_surface.blit(self.tint_surf, (0, 0))

    def run_battle(self):
        """Chạy trận đấu, xử lý các lượt của Player và Opponent"""
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                # Lựa chọn của người chơi
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:  # Tấn công
                        self.battle.player_turn('attack')
                    elif event.key == pygame.K_h:  # Hồi máu
                        self.battle.player_turn('heal')

            # Cập nhật giao diện và UI
            self.battle.update_ui()

            # Lượt của đối thủ
            if self.battle.is_game_over() is None:  # Nếu trận đấu chưa kết thúc
                self.battle.opponent_turn()

            # Kiểm tra kết thúc game
            result = self.battle.is_game_over()
            if result:
                print(result)
                self.running = False

            pygame.display.update()
    
    def run(self):
        intro_screen()
        self.first_one_dialog()
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not self.show_choice:
                    pause_screen(self.display_surface)

            if self.dialogue and self.dialogue.running:
                self.dialogue.update()
            else:
                self.all_sprites.update(dt)

            if self.show_timer == True and self.timer > 0:
                self.timer -= dt
                if self.timer <= 0:
                    self.fill = False
                    self.player.block()
                    self.show_timer = False
                    self.transition(self.third_mission)

            if hasattr(self, 'background') and self.background:
                self.display_surface.blit(self.background, (0, 0))

            if self.fill:
                self.display_surface.fill(BLACK)

            if self.show_choice:
                yes_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50)
                no_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 60, 200, 50)
                self.show_choice_ui(yes_button, no_button)  
                self.handle_choice_input(yes_button, no_button)

            if self.map is not None:
                self.all_sprites.draw(self.player.rect.center)

            if self.show_ui:
                self.ui.draw()

            if self.dialogue and self.dialogue.running:
                self.dialogue.show_dialog()

            if self.dialogue and self.dialogue.show_achievement_text:
                self.dialogue.update_achievement(dt)

            if self.show_timer and self.show_guide:
                self.draw_timer()
                self.show_guide(dt)

            if self.achievement_active == True:
                self.show_achivement(dt)

            self.tint_screen(dt)

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
