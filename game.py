import random
import pygame
import os
from menu import *

class Game:

    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.MAIN_MENU = Menu(self)
        self.HOWTO = HowTo(self)
        self.CREDITS = Credits(self)
        self.CURR_MENU = self.MAIN_MENU

        self.APP_RUNNING = True
        self.PLAYING = True
        self.WIDTH, self.HEIGHT = 900, 500
        self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT = 60, 60
        self.SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Spaceship Fighter")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        self.FPS = 60
        self.VELOCITY = 5
        self.BULLET_VELOCITY = 10
        self.MAX_BULLETS = 10
        self.ASTEROID_VELOCITY = 1
        self.MAX_ASTEROIDS = 1

        self.ASTEROIDS = []

        self.YELLOW_HIT = pygame.USEREVENT + 1
        self.RED_HIT = pygame.USEREVENT + 2

        self.YELLOW_SCORE = 0
        self.RED_SCORE = 0

        self.BORDER = pygame.Rect(self.WIDTH // 2 - 5, 0, 10, self.HEIGHT)

        self.BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullet_hit.mp3'))
        self.BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bullet_fire.mp3'))

        self.HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
        self.WINNER_FONT = pygame.font.SysFont('comicsans', 100)
        self.GENERAL_FONT = pygame.font.SysFont('arial', 25)

        self.YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
        self.YELLOW_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(self.YELLOW_SPACESHIP_IMAGE, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), 270)
        self.RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
        self.RED_SPACESHIP = pygame.transform.rotate(
            pygame.transform.scale(self.RED_SPACESHIP_IMAGE, (self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)), 90)
        self.HEART_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'heart.png')), (30, 30))
        self.ASTEROIDS.append(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'asteroid1.png')), (50, 50)))
        self.ASTEROIDS.append(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'asteroid2.png')), (50, 50)))
        self.ASTEROIDS.append(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'asteroid3.png')), (50, 50)))
        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),
                                                 (self.WIDTH, self.HEIGHT))

        self.PLAYER2_AI = False
        self.PLAYER2_AI_SHOOT_COOLDOWN = 30  # Cooldown time in frames
        self.PLAYER2_AI_SHOOT_TIMER = 0

        self.red_bullets = []


    def draw_surface(self, red_player, yellow_player, yellow_bullets, red_bullets, yellow_health, red_health, yellow_asteroids, red_asteroids):
        self.SURFACE.blit(self.BACKGROUND, (0, 0))
        pygame.draw.rect(self.SURFACE, self.BLACK, self.BORDER)

        player1_text = self.GENERAL_FONT.render("Player 1 ", 1, self.WHITE)
        player2_text = self.GENERAL_FONT.render("Player 2", 1, self.WHITE)
        player1_score = self.GENERAL_FONT.render("Score " + str(self.YELLOW_SCORE), 1, self.WHITE)
        player2_score = self.GENERAL_FONT.render("Score " + str(self.RED_SCORE), 1, self.WHITE)
        self.SURFACE.blit(player1_text, (10, 10))
        self.SURFACE.blit(player2_text, (self.BORDER.x + 20, 10))
        self.SURFACE.blit(player1_score, (10, self.HEIGHT - 40))
        self.SURFACE.blit(player2_score, (self.BORDER.x + self.BORDER.width + 10, self.HEIGHT - 40))

        # Generate Health
        for count in range(yellow_health):
            self.SURFACE.blit(self.HEART_IMAGE, (self.BORDER.x - 40 - count * 30, 10))

        for count in range(red_health):
            self.SURFACE.blit(self.HEART_IMAGE, (self.WIDTH - 40 - count * 30, 10))

        self.SURFACE.blit(self.YELLOW_SPACESHIP, (yellow_player.x, yellow_player.y))
        self.SURFACE.blit(self.RED_SPACESHIP, (red_player.x, red_player.y))

        for bullet in yellow_bullets:
            pygame.draw.rect(self.SURFACE, self.YELLOW, bullet)

        for bullet in red_bullets:
            pygame.draw.rect(self.SURFACE, self.RED, bullet)

        for asteroid in yellow_asteroids:
            self.SURFACE.blit(self.ASTEROIDS[0], (asteroid.x, asteroid.y))

        for asteroid in red_asteroids:
            self.SURFACE.blit(self.ASTEROIDS[0], (asteroid.x, asteroid.y))

        pygame.display.update()


    def handle_yellow_movement(self, keys_pressed, yellow_player):
        if keys_pressed[pygame.K_a] and yellow_player.x - self.VELOCITY > 0:  # Move Left
            yellow_player.x -= self.VELOCITY
        if keys_pressed[pygame.K_d] and yellow_player.x + self.VELOCITY + yellow_player.width < self.BORDER.x - 15:  # Move Right
            yellow_player.x += self.VELOCITY
        if keys_pressed[pygame.K_w] and yellow_player.y - self.VELOCITY > 40:  # Move Up
            yellow_player.y -= self.VELOCITY
        if keys_pressed[pygame.K_s] and yellow_player.y + self.VELOCITY + yellow_player.height + 20 < self.HEIGHT:  # Move Down
            yellow_player.y += self.VELOCITY

    def handle_red_movement(self, keys_pressed, red_player):
        if not self.PLAYER2_AI:
            if keys_pressed[pygame.K_LEFT] and red_player.x - self.VELOCITY > self.BORDER.x + self.BORDER.width + 15:  # Move Left
                red_player.x -= self.VELOCITY
            if keys_pressed[pygame.K_RIGHT] and red_player.x + self.VELOCITY + red_player.width < self.WIDTH:  # Move Right
                red_player.x += self.VELOCITY
            if keys_pressed[pygame.K_UP] and red_player.y - self.VELOCITY > 40:  # Move Up
                red_player.y -= self.VELOCITY
            if keys_pressed[pygame.K_DOWN] and red_player.y + self.VELOCITY + red_player.height + 20 < self.HEIGHT:  # Move Down
                red_player.y += self.VELOCITY
        else:
            # AI Movement
            if not hasattr(self, 'ai_direction'):
                self.ai_direction = random.choice(['left', 'right', 'up', 'down'])
            
            if self.ai_direction == 'left':
                if red_player.x - self.VELOCITY > self.BORDER.x + self.BORDER.width + 15:
                    red_player.x -= self.VELOCITY
                else:
                    self.ai_direction = random.choice(['left', 'right', 'up', 'down'])
            
            elif self.ai_direction == 'right':
                if red_player.x + self.VELOCITY + red_player.width < self.WIDTH:
                    red_player.x += self.VELOCITY
                else:
                    self.ai_direction = random.choice(['left', 'right', 'up', 'down'])
            
            elif self.ai_direction == 'up':
                if red_player.y - self.VELOCITY > 40:
                    red_player.y -= self.VELOCITY
                else:
                    self.ai_direction = random.choice(['left', 'right', 'up', 'down'])
            
            elif self.ai_direction == 'down':
                if red_player.y + self.VELOCITY + red_player.height + 20 < self.HEIGHT:
                    red_player.y += self.VELOCITY
                else:
                    self.ai_direction = random.choice(['left', 'right', 'up', 'down'])

            # Optionally change direction periodically
            if random.random() < 0.01:  # Adjust the probability for direction change
                self.ai_direction = random.choice(['left', 'right', 'up', 'down'])

            # AI Shooting
            self.PLAYER2_AI_SHOOT_TIMER += 1
            if self.PLAYER2_AI_SHOOT_TIMER >= self.PLAYER2_AI_SHOOT_COOLDOWN:
                bullet = pygame.Rect(red_player.x, red_player.y + red_player.height // 2 - 2, 10, 5)
                self.red_bullets.append(bullet)
                self.BULLET_FIRE_SOUND.play()
                self.PLAYER2_AI_SHOOT_TIMER = 0


    def handle_bullets(self, yellow_bullets, red_bullets, yellow_player, red_player):
        for bullet in yellow_bullets:
            bullet.x += self.BULLET_VELOCITY
            if red_player.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.RED_HIT))
                yellow_bullets.remove(bullet)
            elif bullet.x > self.WIDTH:
                yellow_bullets.remove(bullet)

        for bullet in red_bullets:
            bullet.x -= self.BULLET_VELOCITY
            if yellow_player.colliderect(bullet):
                pygame.event.post(pygame.event.Event(self.YELLOW_HIT))
                red_bullets.remove(bullet)
            elif bullet.x < 0:
                red_bullets.remove(bullet)

    def handle_asteroids(self, yellow_asteroids, red_asteroids, yellow_player, red_player):
        for asteroid in yellow_asteroids:
            asteroid.y += self.ASTEROID_VELOCITY
            if yellow_player.colliderect(asteroid):
                pygame.event.post(pygame.event.Event(self.YELLOW_HIT))
                yellow_asteroids.remove(asteroid)
            elif asteroid.y > self.HEIGHT:
                yellow_asteroids.remove(asteroid)

        for asteroid in red_asteroids:
            asteroid.y += self.ASTEROID_VELOCITY
            if red_player.colliderect(asteroid):
                pygame.event.post(pygame.event.Event(self.RED_HIT))
                red_asteroids.remove(asteroid)
            if asteroid.y > self.HEIGHT:
                red_asteroids.remove(asteroid)

    def draw_winner(self, text):
        draw_text = self.WINNER_FONT.render(text, 1, self.WHITE)
        self.SURFACE.blit(draw_text, (self.WIDTH // 2 - draw_text.get_width() // 2, self.HEIGHT // 2 - draw_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(3000)

    def play(self):
        red_player = pygame.Rect(700, 250, self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)
        yellow_player = pygame.Rect(100, 250, self.SPACESHIP_WIDTH, self.SPACESHIP_HEIGHT)

        yellow_bullets = []
        red_bullets = []

        yellow_asteroids = []
        red_asteroids = []

        red_health = 5
        yellow_health = 5

        winner_text = ''
        clock = pygame.time.Clock()
        while self.PLAYING:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.PLAYING = False
                    self.CURR_MENU.RUNNING = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.PLAYING = False
                        break

                    if event.key == pygame.K_LSHIFT and len(yellow_bullets) < self.MAX_BULLETS:
                        bullet = pygame.Rect(yellow_player.x + yellow_player.width,
                                             yellow_player.y + yellow_player.height // 2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        self.BULLET_FIRE_SOUND.play()

                    if not self.PLAYER2_AI:
                        if event.key == pygame.K_RSHIFT and len(red_bullets) < self.MAX_BULLETS:
                            bullet = pygame.Rect(red_player.x, red_player.y + red_player.height // 2 - 2, 10, 5)
                            red_bullets.append(bullet)
                            self.BULLET_FIRE_SOUND.play()

                    if len(yellow_asteroids) < self.MAX_ASTEROIDS:
                        random_x = random.randint(20, self.WIDTH // 2 - 50)
                        asteroid = pygame.Rect(random_x, 50, self.ASTEROIDS[0].get_width() - 5, self.ASTEROIDS[0].get_height() - 5)
                        yellow_asteroids.append(asteroid)

                    if len(red_asteroids) < self.MAX_ASTEROIDS:
                        random_x = random.randint(self.BORDER.x + self.BORDER.width + 20, self.WIDTH - 20)
                        asteroid = pygame.Rect(random_x, 50, self.ASTEROIDS[0].get_width() - 5, self.ASTEROIDS[0].get_height() - 5)
                        red_asteroids.append(asteroid)

                if event.type == self.YELLOW_HIT:
                    yellow_health -= 1
                    self.BULLET_HIT_SOUND.play()

                if event.type == self.RED_HIT:
                    red_health -= 1
                    self.BULLET_HIT_SOUND.play()

            keys_pressed = pygame.key.get_pressed()
            self.handle_yellow_movement(keys_pressed, yellow_player)
            self.handle_red_movement(keys_pressed, red_player)
            self.handle_bullets(yellow_bullets, red_bullets, yellow_player, red_player)
            self.handle_asteroids(yellow_asteroids, red_asteroids, yellow_player, red_player)
            self.draw_surface(red_player, yellow_player, yellow_bullets, red_bullets, yellow_health, red_health, yellow_asteroids, red_asteroids)

            if yellow_health <= 0:
                winner_text = "PLAYER 2 WINS!"
                self.RED_SCORE += 100
            if red_health <= 0:
                winner_text = "PLAYER 1 WINS!"
                self.YELLOW_SCORE += 100
            if winner_text != '':
                self.draw_winner(winner_text)
                self.play()

        self.PLAYING = False
