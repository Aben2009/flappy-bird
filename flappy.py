#!/usr/bin/env python3
"""
Flappy Bird - simple clone using Pygame

Usage:
  pip install pygame
  python flappy.py

Controls:
 - SPACE or Left mouse click: flap / start / restart
 - R: restart after game over
 - ESC / window close: quit
"""
import sys
import random
import math
import pygame

# ---------- Configuration ----------
WIDTH, HEIGHT = 400, 600
FPS = 60

BIRD_X = 80
BIRD_RADIUS = 16

GRAVITY = 0.45
FLAP_STRENGTH = -8.5
MAX_FALL_SPEED = 12

PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_DISTANCE = 230  # approx horizontal distance between pipe pairs
PIPE_SPEED = 2.8

GROUND_HEIGHT = 100

BG_COLOR = (135, 206, 235)  # sky blue
BIRD_COLOR = (255, 210, 50)  # yellow
PIPE_COLOR = (34, 139, 34)  # green
PIPE_DARK = (0, 100, 0)
GROUND_COLOR = (222, 184, 135)  # sandy / ground
TEXT_COLOR = (30, 30, 30)

# ---------- Helper classes ----------
class Bird:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = BIRD_X
        self.y = HEIGHT // 2
        self.vel = 0.0
        self.radius = BIRD_RADIUS
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.alive = True
        self.rotation = 0.0  # for simple tilt effect

    def flap(self):
        self.vel = FLAP_STRENGTH

    def update(self):
        self.vel += GRAVITY
        if self.vel > MAX_FALL_SPEED:
            self.vel = MAX_FALL_SPEED
        self.y += self.vel
        # rotation approximate: tilt up when going up, down when falling
        self.rotation = max(-25, min(90, -self.vel * 4))
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius),
                                self.radius * 2, self.radius * 2)

    def draw(self, surf):
        # draw body (circle)
        pygame.draw.circle(surf, BIRD_COLOR, (int(self.x), int(self.y)), self.radius)
        # simple wing
        wing_points = [
            (int(self.x - self.radius*0.2), int(self.y)),
            (int(self.x + self.radius*0.6), int(self.y - self.radius*0.6)),
            (int(self.x + self.radius*0.2), int(self.y))
        ]
        pygame.draw.polygon(surf, (230, 180, 30), wing_points)
        # eye
        eye_x = int(self.x + self.radius * 0.35)
        eye_y = int(self.y - self.radius * 0.35)
        pygame.draw.circle(surf, (0, 0, 0), (eye_x, eye_y), max(2, int(self.radius * 0.2)))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        # ensure gap fits between top and ground
        top_min = 60
        top_max = HEIGHT - GROUND_HEIGHT - 60 - self.gap
        if top_max < top_min:
            top_max = top_min
        self.top = random.randint(top_min, top_max)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def off_screen(self):
        return self.x + self.width < -50

    def collides_with(self, bird_rect):
        top_rect = pygame.Rect(int(self.x), 0, self.width, int(self.top))
        bot_rect = pygame.Rect(int(self.x), int(self.top + self.gap), self.width,
                               HEIGHT - GROUND_HEIGHT - (self.top + self.gap))
        return top_rect.colliderect(bird_rect) or bot_rect.colliderect(bird_rect)

    def draw(self, surf):
        top_rect = pygame.Rect(int(self.x), 0, self.width, int(self.top))
        bot_rect = pygame.Rect(int(self.x), int(self.top + self.gap), self.width,
                               HEIGHT - GROUND_HEIGHT - (self.top + self.gap))
        pygame.draw.rect(surf, PIPE_COLOR, top_rect)
        pygame.draw.rect(surf, PIPE_COLOR, bot_rect)
        # pipe caps for nicer look
        cap_h = 18
        pygame.draw.rect(surf, PIPE_DARK, pygame.Rect(int(self.x - 2), int(self.top - cap_h),
                                                      self.width + 4, cap_h))
        pygame.draw.rect(surf, PIPE_DARK, pygame.Rect(int(self.x - 2), int(self.top + self.gap),
                                                      self.width + 4, cap_h))

# ---------- Utility functions ----------
def draw_text_center(surf, text, size, y, fontname=None, color=TEXT_COLOR):
    font = pygame.font.SysFont(fontname, size, bold=True)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(WIDTH//2, y))
    surf.blit(render, rect)

def reset_game(state):
    state['bird'].reset()
    state['pipes'].clear()
    # create initial pipes: a couple spaced out
    start_x = WIDTH + 60
    for i in range(3):
        state['pipes'].append(Pipe(start_x + i * PIPE_DISTANCE))
    state['score'] = 0
    state['high_score'] = state.get('high_score', 0)
    state['frame'] = 0
    state['game_state'] = 'start'

# ---------- Main ----------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy - Simple")
    clock = pygame.time.Clock()

    # game state container
    state = {}
    state['bird'] = Bird()
    state['pipes'] = []
    state['score'] = 0
    state['high_score'] = 0
    state['frame'] = 0
    state['game_state'] = 'start'  # 'start', 'playing', 'gameover'

    reset_game(state)

    running = True
    while running:
        clock.tick(FPS)
        state['frame'] += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if state['game_state'] == 'start':
                        state['game_state'] = 'playing'
                        state['bird'].flap()
                    elif state['game_state'] == 'playing':
                        state['bird'].flap()
                    elif state['game_state'] == 'gameover':
                        # restart
                        reset_game(state)
                elif event.key == pygame.K_r:
                    reset_game(state)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if state['game_state'] == 'start':
                        state['game_state'] = 'playing'
                        state['bird'].flap()
                    elif state['game_state'] == 'playing':
                        state['bird'].flap()
                    elif state['game_state'] == 'gameover':
                        reset_game(state)

        # update
        if state['game_state'] == 'playing':
            state['bird'].update()
            # spawn new pipes as needed
            if len(state['pipes']) == 0 or (state['pipes'][-1].x < WIDTH - PIPE_DISTANCE):
                state['pipes'].append(Pipe(WIDTH + 10))

            for p in state['pipes']:
                p.update()

            # remove off-screen pipes
            state['pipes'] = [p for p in state['pipes'] if not p.off_screen()]

            # scoring & collision detection
            for p in state['pipes']:
                # score when first passes bird
                if not p.passed and p.x + p.width < state['bird'].x:
                    p.passed = True
                    state['score'] += 1
                    if state['score'] > state['high_score']:
                        state['high_score'] = state['score']

                if p.collides_with(state['bird'].rect):
                    state['game_state'] = 'gameover'
                    state['bird'].alive = False

            # collision with ground or ceiling
            if state['bird'].y + state['bird'].radius >= HEIGHT - GROUND_HEIGHT:
                state['bird'].y = HEIGHT - GROUND_HEIGHT - state['bird'].radius
                state['game_state'] = 'gameover'
                state['bird'].alive = False
            if state['bird'].y - state['bird'].radius <= 0:
                state['bird'].y = state['bird'].radius
                state['bird'].vel = 0

        elif state['game_state'] in ('start', 'gameover'):
            # animate bird little up-down on start screen
            
            if state['game_state'] == 'start':
                state['bird'].y = HEIGHT//2 + (3 * math.sin(state['frame'] * 0.08))
            state['bird'].rect = pygame.Rect(int(state['bird'].x - state['bird'].radius),
                                             int(state['bird'].y - state['bird'].radius),
                                             state['bird'].radius*2, state['bird'].radius*2)

        # draw
        screen.fill(BG_COLOR)

        # background simple (could add clouds etc.)
        # pipes
        for p in state['pipes']:
            p.draw(screen)

        # ground
        pygame.draw.rect(screen, GROUND_COLOR, pygame.Rect(0, HEIGHT - GROUND_HEIGHT, WIDTH, GROUND_HEIGHT))

        # bird
        state['bird'].draw(screen)

        # UI / texts
        if state['game_state'] == 'start':
            draw_text_center(screen, "FLAPPY - Simple", 34, HEIGHT * 0.22)
            draw_text_center(screen, "Press SPACE or click to start", 20, HEIGHT * 0.32)
            draw_text_center(screen, "Tap to flap", 18, HEIGHT * 0.38)
            draw_text_center(screen, f"High score: {state['high_score']}", 18, HEIGHT * 0.46)
        elif state['game_state'] == 'playing':
            draw_text_center(screen, str(state['score']), 48, HEIGHT * 0.12)
        elif state['game_state'] == 'gameover':
            draw_text_center(screen, "GAME OVER", 46, HEIGHT * 0.30)
            draw_text_center(screen, f"Score: {state['score']}", 28, HEIGHT * 0.42)
            draw_text_center(screen, f"High score: {state['high_score']}", 22, HEIGHT * 0.50)
            draw_text_center(screen, "Press R to restart or SPACE / click", 18, HEIGHT * 0.62)

        # small instruction at bottom
        draw_text_center(screen, "ESC to quit", 14, HEIGHT - 18, color=(80,80,80))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()