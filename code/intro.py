import pygame
import sys
from settings import *

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Blazor Vortex (Demo)")
font = pygame.font.Font('data/fonts/SVN-Retron 2000.otf', 74)
button_font = pygame.font.Font('data/fonts/SVN-Retron 2000.otf', 40)

# Hàm vẽ màn hình intro
def draw_intro_screen():
    screen.fill(BLACK)

    # Vẽ tiêu đề
    title_text = font.render("Blazor Vortex (Demo)", True, BLACK)
    title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
    screen.blit(title_text, title_rect)

    # Vẽ các nút
    start_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50)
    quit_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 50)

    # Nút "Vào Game"
    pygame.draw.rect(screen, BUTTON_COLOR, start_button)
    start_text = button_font.render("Vào Game", True, WHITE)
    screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + (start_button.height - start_text.get_height()) // 2))

    # Nút "Thoát Game"
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button)
    quit_text = button_font.render("Thoát Game", True, WHITE)
    screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2, quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

    pygame.display.update()

    return start_button, quit_button

# Hàm xử lý sự kiện
def intro_screen():
    running = True
    while running:
        start_button, quit_button = draw_intro_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Kiểm tra chuột di chuyển để đổi màu nút
            if event.type == pygame.MOUSEMOTION:
                if start_button.collidepoint(event.pos):
                    pygame.draw.rect(screen, HOVER_COLOR, start_button)
                else:
                    pygame.draw.rect(screen, BUTTON_COLOR, start_button)
                
                if quit_button.collidepoint(event.pos):
                    pygame.draw.rect(screen, HOVER_COLOR, quit_button)
                else:
                    pygame.draw.rect(screen, BUTTON_COLOR, quit_button)

            # Kiểm tra nhấn chuột
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    print("Vào Game!")
                    return True  # Trả về True khi người chơi nhấn "Vào Game"
                elif quit_button.collidepoint(event.pos):
                    print("Thoát Game!")
                    running = False  # Thoát khỏi màn hình intro

        pygame.display.update()

    pygame.quit()
    sys.exit()

