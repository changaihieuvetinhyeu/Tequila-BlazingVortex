import pygame
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from mission import Mission
from ui import UI
from intro import intro_screen,pause_screen

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Blazing Vortex")
        self.clock = pygame.time.Clock()
        self.running = True

        # Groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Mission/Dialogues
        self.show_timer = False
        self.finished = False
        self.dialogue = None
        self.timer = 60
        self.fill = False
        self.guide_active = False

        #tint
        self.tint_surf = pygame.Surface((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.tint_mode = 'untint'
        self.tint_progress = 255
        self.tint_direction = -1
        self.tint_speed = 600
        

        # Setup
        self.show_ui = False
        self.map = None
        self.player = None
        self.ui = UI(self)
        # self.load_images()
        
    # def load_images(self):
    #     folders = list(walk(join("images", "enemies")))[0][1]
    #     self.enemy_frames = {}
    #     for folder in folders:
    #         for folder_path, _, file_names in walk(join("images", "enemies", folder)):
    #             self.enemy_frames[folder] = []
    #             for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
    #                 full_path = join(folder_path, file_name)
    #                 surf = pygame.image.load(full_path).convert_alpha()
    #                 self.enemy_frames[folder].append(surf)

    def clear_sprites(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.enemy_sprites.empty()

    def setup(self, map_name):
        map = load_pygame(join("data", "maps", map_name))
        self.map = map
        ground_layer = map.get_layer_by_name("Ground")
        if ground_layer:
            for x, y, image in ground_layer.tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        objects_layer = map.get_layer_by_name("Objects")
        if objects_layer:
            for obj in objects_layer:
                CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        collisions_layer = map.get_layer_by_name("Collisions")
        if collisions_layer:
            for obj in collisions_layer:
                CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        entities_layer = map.get_layer_by_name("Entities")
        if entities_layer:
            for obj in entities_layer:
                if obj.name == "Player":
                    self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                # else:
                #     Enemy(
                #         (obj.x, obj.y),
                #         choice(list(self.enemy_frames.values())),
                #         (self.all_sprites, self.enemy_sprites),
                #         self.player,
                #         self.collision_sprites,
                #     )
    
    def first_one_dialog(self):
        self.background = pygame.image.load('images/background/controversy.jpeg').convert()
        self.background = pygame.transform.scale(self.background,(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background,(0,0))
        self.dialogue = Mission(
            self,
            [
                "Minh Hàn: Mày học hành kiểu gì thế này?",
                "Thời Đăng: Kệ tao",
                "Minh Hàn: Học hành thế này thi cử sao được",
                "Thời Đăng: Sao mày nói nhiều thế nhỉ ? Tao tạch thì liên quan gì đến mày ?",
                "Minh Hàn: Mày nói thế mà cũng nói được à",
            ],
            fill_screen = False,
            sound_file = None,
            on_complete=lambda: self.transition(self.first_two_dialog)
        )
    
    def first_two_dialog(self):
        self.background = pygame.image.load('images/background/fight1.png').convert()
        self.background = pygame.transform.scale(self.background,(WINDOW_WIDTH, WINDOW_HEIGHT))

        self.display_surface.blit(self.background,(0,0))
        self.dialogue = Mission(
            self,
            [
                "Thời Đăng: Tao thích nói thế đấy! Giỏi vào đánh nhau xem nào ?",
            ],
            fill_screen = False,
            sound_file = None,
            on_complete=lambda: self.transition(self.second_one_dialogue)
        )

    def second_one_dialogue(self):
        self.background = pygame.image.load('images/background/defeat1.png').convert()
        self.background = pygame.transform.scale(self.background,(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background,(0,0))
        self.dialogue = Mission(
            self,
            [
                "Minh Hàn: Ơ kia Thời Đăng dậy đi",
                "Thời Đăng: ...",
                "Minh Hàn: Ơ kìa mày làm sao thế dậy đi !!!",
                "Thời Đăng: ...",
            ],
            fill_screen = False,
            sound_file = 'sound/punch.mp3',
            on_complete=lambda: self.transition(self.second_two_dialogue)
        )
    
    def second_two_dialogue(self):
        self.background = pygame.image.load('images/background/wakinup.jpeg').convert()
        self.background = pygame.transform.scale(self.background,(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background,(0,0))
        self.dialogue = Mission(
            self,
            [
                "Thời Đăng: Đây là đâu? Sao mình lại ở đây?", 
                "Thời Đăng: Làm sao để thoát khỏi nơi này?",
            ],
            fill_screen = False,
            sound_file = None,
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
        self.guide_x = self.display_surface.get_width()  
        self.show_timer = True
        self.timer = 60


    def third_mission(self):
        self.clear_sprites()
        self.show_timer = False
        self.background = pygame.image.load('images/background/firstmeet.jpg').convert()
        self.background = pygame.transform.scale(self.background,(WINDOW_WIDTH, WINDOW_HEIGHT))
        self.display_surface.blit(self.background, (0, -100))
        self.dialogue = Mission(
            self,
            [
                "???: Chào cậu bé",
                "Thời Đăng: Ông là ai ?",
                "???: Cậu không cần biết ta là ai",
                "Thời Đăng: Vậy thì tại sao ông ở đây ?",
                "???: Ta ở đây để giúp cậu một việc",
                "Thời Đăng: Việc gì ?",
                "???: Ta trông thấy cậu có vẻ đang gặp khó khăn với kì thi ở trên trường",
                "Thời Đăng: Tôi vẫn ổn không có vấn đề gì cả, chỉ là hơi lơ đễnh một chút thôi",
                "???: Vậy ta ở đây để giúp cậu đạt được kết quả tốt trong kì thi sắp tới",
                "Thời Đăng: Việc này tôi cần suy nghĩ một chút đã...",
                "???: Cần gì phải suy nghĩ, cậu nhìn bạn bè cậu chê cười mà không thấy xấu hổ sao ?",
                "Thời Đăng: Nhưng...",
                "???: Không nhưng gì hết, cậu có muốn giúp ta giúp một tay không. Suy nghĩ nhanh rồi trả lời !"
            ],
            sound_file=None,
            on_complete=lambda: self.transition(self.end_of_demo)
        )
        
    def end_of_demo(self):
        self.fill = True
        self.dialogue = Mission(
            self,
            [
                "Liệu quyết định của Thần Đăng là gì ?",
                "Liệu Thời Đăng sẽ trả lời như nào ?",
                "Hãy cùng đón chờ nhé"
            ],
            fill_screen = True,
            on_complete=lambda: self.transition(self.restart_game)
        )
        self.dialogue.show_dialog = self.dialogue.show_centered_text

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
        font = pygame.font.Font("data/fonts/FVF Fernando 08.ttf", 32)
        timer_text = font.render(f"Thời gian còn lại: {int(self.timer)}", True, WHITE)
        self.display_surface.blit(timer_text, (10, 10))

    def unblock_player_after_dialogue(self):
        self.dialogue = None
        self.player.unblock()

    def transition(self,next_mission):
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

        font = pygame.font.Font('data/fonts/FVF Fernando 08.ttf', 18)
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

        # Hiệu ứng trượt
        target_x = self.display_surface.get_width() - guide_width - 20 
        if self.guide_active:
            if self.guide_x > target_x:  
                self.guide_x = max(self.guide_x - 600 * dt, target_x)  
            elif pygame.time.get_ticks() - self.guide_timer > 5000:  
                self.guide_active = False  
        else:
            if self.guide_x < self.display_surface.get_width():  
                self.guide_x += 600 * dt

        # Vẽ bảng hướng dẫn
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

    

    def run(self):
        intro_screen()
        self.first_one_dialog()
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
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

            if self.map is not None:
                self.all_sprites.draw(self.player.rect.center)

            if self.show_ui:
                self.ui.draw()

            if self.dialogue and self.dialogue.running:
                self.dialogue.show_dialog()

            if self.show_timer and self.show_guide:
                self.draw_timer()
                self.show_guide(dt)

            self.tint_screen(dt)
            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()