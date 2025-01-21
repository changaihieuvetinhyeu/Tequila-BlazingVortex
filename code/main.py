import pygame
from settings import *
from player import Player
from sprites import *
from pytmx.util_pygame import load_pygame
from groups import AllSprites
from mission import Mission
from ui import UI
from random import choice

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Blazer Vortex")
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

        # Setup
        self.player = None
        self.ui = UI(self)
        self.load_images()
        self.setup('world.tmx')

    def load_images(self):
        folders = list(walk(join("images", "enemies")))[0][1]
        self.enemy_frames = {}
        for folder in folders:
            for folder_path, _, file_names in walk(join("images", "enemies", folder)):
                self.enemy_frames[folder] = []
                for file_name in sorted(file_names, key=lambda name: int(name.split(".")[0])):
                    full_path = join(folder_path, file_name)
                    surf = pygame.image.load(full_path).convert_alpha()
                    self.enemy_frames[folder].append(surf)

    def clear_sprites(self):
        self.all_sprites.empty()
        self.collision_sprites.empty()
        self.enemy_sprites.empty()

    def setup(self, map_name):
        map = load_pygame(join("data", "maps", map_name))

        # Kiểm tra và vẽ layer 'Ground'
        ground_layer = map.get_layer_by_name("Ground")
        if ground_layer:
            for x, y, image in ground_layer.tiles():
                Sprite((x * TILE_SIZE, y * TILE_SIZE), image, self.all_sprites)

        # Kiểm tra và vẽ layer 'Objects'
        objects_layer = map.get_layer_by_name("Objects")
        if objects_layer:
            for obj in objects_layer:
                CollisionSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

        # Kiểm tra và vẽ layer 'Collisions'
        collisions_layer = map.get_layer_by_name("Collisions")
        if collisions_layer:
            for obj in collisions_layer:
                CollisionSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

        # Kiểm tra và vẽ layer 'Entities'
        entities_layer = map.get_layer_by_name("Entities")
        if entities_layer:
            for obj in entities_layer:
                if obj.name == "Player":
                    self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites)
                else:
                    Enemy(
                        (obj.x, obj.y),
                        choice(list(self.enemy_frames.values())),
                        (self.all_sprites, self.enemy_sprites),
                        self.player,
                        self.collision_sprites,
                    )

    def handle_attack(self):
        for enemy in self.enemy_sprites:
            if enemy.defeated:
                continue
            player_pos = pygame.Vector2(self.player.rect.center)
            enemy_pos = pygame.Vector2(enemy.rect.center)
            distance = player_pos.distance_to(enemy_pos)
            if distance < 100:
                enemy.take_damage(10)
                if enemy.health <= 0:
                    enemy.defeated = True
                    self.finished = True

        # Kiểm tra nếu tất cả Enemy đã bị đánh bại
        self.check_all_enemies_defeated()

    def check_all_enemies_defeated(self):
        if all(enemy.defeated for enemy in self.enemy_sprites):
            self.second_mission()

    def first_mission(self):
        self.dialogue = Mission(
            self,
            [
                "Minh Hàn: Mày học hành kiểu đéo gì thế này?",
                "Thời Đăng: Kệ mẹ tao.",
                "Minh Hàn: Thích thì đánh mẹ nhau đi!",
            ],
            fill_screen = True
        )
        self.show_ui = True

    def second_mission(self):
        self.clear_sprites()
        self.show_ui = False
        self.setup('first.tmx')
        self.dialogue = Mission(
            self,
            [
                "Thời Đăng: Đây là đâu? Sao mình lại ở đây?",
                "Thời Đăng: Mình phải tìm cách thoát khỏi nơi này.",
            ],
            fill_screen = True,
            on_complete=self.unblock_player_after_dialogue,
        )
        self.timer = 5
        self.show_timer = True

    def third_mission(self):
        self.clear_sprites()
        self.show_timer = False
        self.background = pygame.image.load('images/background/firstmeet.jpg').convert()
        self.display_surface.blit(self.background, (0, 0))
        self.dialogue = Mission(
            self,
            [
                "???: Chào cậu bé",
                "Thời Đăng: Ông là ai ?",
                "???: Cậu không cần biết ta là ai",
                "Thời Đăng: Vậy thì tại sao ông ở đây ?",
                "???: Ta ở đây để giúp cậu một việc ?",
                "Thời Đăng: Việc gì ?",
                "???: Ta trông thấy cậu có vẻ đang gặp khó khăn với kì thi ở trên trường",
                "Thời Đăng: Tôi vẫn ổn không có vấn đề gì cả, chỉ là hơi lơ đễnh một chút thôi",
                "???: Vậy ta ở đây để giúp cậu đạt được kết quả tốt trong kì thi sắp tới",
                "Thời Đăng: Việc này tôi cần suy nghĩ một chút đã...",
                "???: Cần gì phải suy nghĩ, cậu nhìn bạn bè cậu chê cười mà không thấy xấu hổ sao ?",
                "Thời Đăng: Nhưng...",
                "???: Không nhưng gì hết, cậu có muốn giúp ta giúp một tay không. Suy nghĩ nhanh rồi trả lời !"
            ],
            on_complete=self.end_of_demo
        )

    def end_of_demo(self):
        self.dialogue = Mission(
            self,
            [
                "Liệu quyết định của Thần Đăng là gì ?",
                "Liệu anh ấy sẽ trả lời như nào ?",
                "Hãy đón chờ ở phiên bản sắp tới !"
            ],
            fill_screen = True,
            on_complete=self.quit_game
        )
        self.dialogue.show_dialog = self.dialogue.show_centered_text

    def quit_game(self):
        self.running = False

    def draw_timer(self):
        font = pygame.font.Font("data/fonts/SVN-Retron 2000.otf", 36)
        timer_text = font.render(f"Thời gian còn lại: {int(self.timer)}", True, (255, 255, 255))
        self.display_surface.blit(timer_text, (10, 10))

    def unblock_player_after_dialogue(self):
        self.dialogue = None
        self.player.unblock()

    def run(self):
        self.first_mission()
        while self.running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.finished:
                    self.handle_attack()

            if self.dialogue and self.dialogue.running:
                self.dialogue.update()
            else:
                self.all_sprites.update(dt)

            if self.show_timer and self.timer > 0:
                self.timer -= dt
                if self.timer <= 0:
                    self.third_mission()

            # if self.dialogue.fill_screen:
            #     self.display_surface.fill(BLACK)

            self.all_sprites.draw(self.player.rect.center)

            if self.show_ui:
                self.ui.draw()

            if self.dialogue and self.dialogue.running:
                self.dialogue.show_dialog()

            if self.show_timer:
                self.draw_timer()

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()