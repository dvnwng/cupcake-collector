import pygame
import sys
import random
import asyncio

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cupcake Collector")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
YELLOW = (255, 223, 0)

font_large = pygame.font.SysFont("Arial", 48)
font_small = pygame.font.SysFont("Arial", 24)

async def main():
    bg_img = pygame.image.load("Sonic_Background.png").convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

    player_img = pygame.image.load("sonic.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (40, 50))

    platform_img = pygame.image.load("sonic_platform.png").convert_alpha()

    ring_img = pygame.image.load("sonic_ring.png").convert_alpha()
    ring_img = pygame.transform.scale(ring_img, (24, 24))

    player_rect = pygame.Rect(100, 450, 40, 50)
    player_vel_x = 0
    player_vel_y = 0
    player_speed = 6

    GRAVITY = 0.7
    JUMP_STRENGTH = -14
    is_grounded = False

    platforms = [
        pygame.Rect(0, 530, 800, 70),
        pygame.Rect(100, 410, 220, 25),
        pygame.Rect(450, 320, 220, 25),
        pygame.Rect(200, 200, 200, 25)
    ]

    platform_imgs = []
    for p in platforms:
        scaled = pygame.transform.scale(platform_img, (p.width, p.height))
        platform_imgs.append(scaled)

    rings = []
    for i in range(12):
        rx = random.randint(50, 750)
        ry = random.randint(80, 480)
        rings.append(pygame.Rect(rx, ry, 24, 24))

    game_state = "START"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_state == "START" or game_state == "WIN":
                    player_rect.x = 100
                    player_rect.y = 450
                    player_vel_x = 0
                    player_vel_y = 0
                    
                    rings = []
                    for i in range(12):
                        rx = random.randint(50, 750)
                        ry = random.randint(80, 480)
                        rings.append(pygame.Rect(rx, ry, 24, 24))
                    
                    game_state = "PLAYING"

        if game_state == "PLAYING":
            keys = pygame.key.get_pressed()
            player_vel_x = 0
            
            if keys[pygame.K_LEFT]:
                player_vel_x = -player_speed
            if keys[pygame.K_RIGHT]:
                player_vel_x = player_speed
            if keys[pygame.K_UP] and is_grounded:
                player_vel_y = JUMP_STRENGTH
                is_grounded = False

            player_vel_y += GRAVITY

            player_rect.x += player_vel_x
            if player_rect.left < 0:
                player_rect.left = 0
            if player_rect.right > WIDTH:
                player_rect.right = WIDTH

            player_rect.y += player_vel_y
            is_grounded = False  
            
            for p in platforms:
                if player_rect.colliderect(p):
                    if player_vel_y > 0:
                        player_rect.bottom = p.top
                        player_vel_y = 0
                        is_grounded = True
                    elif player_vel_y < 0:
                        player_rect.top = p.bottom
                        player_vel_y = 0

            for ring in rings[:]:
                if player_rect.colliderect(ring):
                    rings.remove(ring)

            if len(rings) == 0:
                game_state = "WIN"

        screen.blit(bg_img, (0, 0))

        if game_state == "START":
            title_text = font_large.render("Sonic Ring Collector", True, YELLOW)
            start_text = font_small.render("Click Anywhere to Start", True, WHITE)
            screen.blit(title_text, (200, 220))
            screen.blit(start_text, (270, 300))

        elif game_state == "PLAYING" or game_state == "WIN":
            for i in range(len(platforms)):
                screen.blit(platform_imgs[i], (platforms[i].x, platforms[i].y))

            for ring in rings:
                screen.blit(ring_img, (ring.x, ring.y))

            screen.blit(player_img, (player_rect.x, player_rect.y))

            score_text = font_small.render("Rings Left: " + str(len(rings)), True, WHITE)
            screen.blit(score_text, (20, 20))

            if game_state == "WIN":
                win_text = font_large.render("Stage Cleared!", True, YELLOW)
                restart_text = font_small.render("Click Anywhere to Play Again", True, WHITE)
                screen.blit(win_text, (260, 220))
                screen.blit(restart_text, (240, 300))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    asyncio.run(main())
