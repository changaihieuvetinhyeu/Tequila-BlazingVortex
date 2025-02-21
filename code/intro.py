import pygame
import sys
from settings import *

pygame.init()

def intro_screen():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Blazing Vortex (Demo)")

    title_font = pygame.font.Font('C:/Users/Dell/Downloads/Game concept/Graphics/Tequila-BlazingVortex-main/data/fonts/FVF Fernando 08.ttf', 74)
    button_font = pygame.font.Font('C:/Users/Dell/Downloads/Game concept/Graphics/Tequila-BlazingVortex-main/data/fonts/FVF Fernando 08.ttf', 40)

    background = pygame.image.load('C:/Users/Dell/Downloads/Game concept/Graphics/Tequila-BlazingVortex-main/images/background/mainmenu.jpg').convert()
    background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))

    def draw_intro_screen(mouse_pos):
        screen.blit(background, (0, 0))

        title_text = title_font.render("Blazer Vortex", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))
        screen.blit(title_text, title_rect)

        start_text = button_font.render("Bắt đầu", True, WHITE)
        settings_text = button_font.render("Cài Đặt", True, WHITE)
        quit_text = button_font.render("Thoát", True, WHITE)

        max_width = max(start_text.get_width(), settings_text.get_width(), quit_text.get_width()) + 40  
        button_height = max(start_text.get_height(), settings_text.get_height(), quit_text.get_height()) + 20

        start_button = pygame.Rect(WINDOW_WIDTH // 2 - max_width // 2, WINDOW_HEIGHT // 2 - 100, max_width, button_height)
        settings_button = pygame.Rect(WINDOW_WIDTH // 2 - max_width // 2, WINDOW_HEIGHT // 2 + 50, max_width, button_height)
        quit_button = pygame.Rect(WINDOW_WIDTH // 2 - max_width // 2, WINDOW_HEIGHT // 2 + 50, max_width, button_height)

        start_color = HOVER_COLOR if start_button.collidepoint(mouse_pos) else BUTTON_COLOR
        settings_color = HOVER_COLOR if settings_button.collidepoint(mouse_pos) else BUTTON_COLOR
        quit_color = HOVER_COLOR if quit_button.collidepoint(mouse_pos) else BUTTON_COLOR

        # Vẽ nút bo tròn
        pygame.draw.rect(screen, start_color, start_button, border_radius=15)
        screen.blit(
            start_text,
            (start_button.x + (start_button.width - start_text.get_width()) // 2,
             start_button.y + (start_button.height - start_text.get_height()) // 2),
        )

        # pygame.draw.rect(screen, settings_color, settings_button, border_radius=15)
        # screen.blit(
        #     settings_text,
        #     (settings_button.x + (settings_button.width - settings_text.get_width()) // 2,
        #      settings_button.y + (settings_button.height - settings_text.get_height()) // 2),
        # )

        pygame.draw.rect(screen, quit_color, quit_button, border_radius=15)
        screen.blit(
            quit_text,
            (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
             quit_button.y + (quit_button.height - quit_text.get_height()) // 2),
        )

        pygame.display.update()

        return start_button, settings_button, quit_button

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos() 
        start_button, settings_button, quit_button = draw_intro_screen(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button.collidepoint(event.pos):
                    return  
                elif quit_button.collidepoint(event.pos):
                    running = False  

    pygame.quit()
    sys.exit()

def pause_screen(screen):
    pause_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)  
    clock = pygame.time.Clock()

    alpha = 0  
    tint_speed = 300  

    title_font = pygame.font.Font('C:/Users/Dell/Downloads/Game concept/Graphics/Tequila-BlazingVortex-main/data/fonts/FVF Fernando 08.ttf', 74)
    button_font = pygame.font.Font('C:/Users/Dell/Downloads/Game concept/Graphics/Tequila-BlazingVortex-main/data/fonts/FVF Fernando 08.ttf', 40)

    def draw_pause_screen(mouse_pos, alpha):
        pause_overlay.fill((0, 0, 0, alpha))
        screen.blit(pause_overlay, (0, 0)) 

        title_text = title_font.render("Tạm dừng", True, WHITE)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 5))
        screen.blit(title_text, title_rect)

        resume_text = button_font.render("Quay lại", True, WHITE)
        quit_text = button_font.render("Thoát", True, WHITE)

        max_width = max(resume_text.get_width(), quit_text.get_width()) + 40
        button_height = max(resume_text.get_height(), quit_text.get_height()) + 20

        resume_button = pygame.Rect(WINDOW_WIDTH // 2 - max_width // 2, WINDOW_HEIGHT // 2 - 100, max_width, button_height)
        quit_button = pygame.Rect(WINDOW_WIDTH // 2 - max_width // 2, WINDOW_HEIGHT // 2 + 50, max_width, button_height)

        resume_color = HOVER_COLOR if resume_button.collidepoint(mouse_pos) else BUTTON_COLOR
        quit_color = HOVER_COLOR if quit_button.collidepoint(mouse_pos) else BUTTON_COLOR

        pygame.draw.rect(screen, resume_color, resume_button, border_radius=15)
        screen.blit(
            resume_text,
            (resume_button.x + (resume_button.width - resume_text.get_width()) // 2,
             resume_button.y + (resume_button.height - resume_text.get_height()) // 2),
        )

        pygame.draw.rect(screen, quit_color, quit_button, border_radius=15)
        screen.blit(
            quit_text,
            (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
             quit_button.y + (quit_button.height - quit_text.get_height()) // 2),
        )

        pygame.display.update()
        return resume_button, quit_button

    running = True
    fade_in_complete = False  

    while running:
        dt = clock.tick(60) / 1000  
        mouse_pos = pygame.mouse.get_pos()

        # Tăng alpha dần dần
        if not fade_in_complete:
            alpha += tint_speed * dt
            if alpha >= 150:  
                alpha = 150
                fade_in_complete = True

        resume_button, quit_button = draw_pause_screen(mouse_pos, int(alpha))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume_button.collidepoint(event.pos):
                    return "resume"  
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
        clock.tick(60)  

