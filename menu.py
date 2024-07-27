import pygame
import os


class Menu:

    def __init__(self, game):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.game = game
        self.RUNNING = True
        self.WIDTH, self.HEIGHT = 900, 500
        self.SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        self.CURSOR_OFFSET = 50
        self.CURSOR_STATE = "start"

        pygame.display.set_caption("Spaceship Fighter")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        self.FPS = 60

        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'menu_bg.png')),
                                                 (self.WIDTH, self.HEIGHT))
        self.CURSOR_IMAGE = pygame.image.load(os.path.join('Assets', 'right-arrow.png'))
        self.CURSOR = pygame.transform.scale(self.CURSOR_IMAGE, (40, 40))

        self.GAME_NAME_FONT = pygame.font.SysFont('comicsans', 60)
        self.MENU_OPTIONS_FONT = pygame.font.SysFont('comicsans', 40)

        self.GAME_NAME_TEXT = self.GAME_NAME_FONT.render("SPACESHIP FIGHTER", 1, self.WHITE)
        self.START_GAME_TEXT = self.MENU_OPTIONS_FONT.render("START  GAME", 1, self.WHITE)
        self.HOW_TO_PLAY_TEXT = self.MENU_OPTIONS_FONT.render("HOW TO PLAY", 1, self.WHITE)
        self.CREDITS_TEXT = self.MENU_OPTIONS_FONT.render("CREDITS", 1, self.WHITE)
        self.PLAYER2_TEXT = self.MENU_OPTIONS_FONT.render("PLAYER 2: AI", 1, self.WHITE)

        self.START_X, self.START_Y = self.WIDTH // 2 - self.START_GAME_TEXT.get_width() // 2, 210
        self.HOWTO_X, self.HOWTO_Y = self.WIDTH // 2 - self.HOW_TO_PLAY_TEXT.get_width() // 2, 270
        self.CREDITS_X, self.CREDITS_Y = self.WIDTH // 2 - self.CREDITS_TEXT.get_width() // 2, 330
        self.PLAYER2_X, self.PLAYER2_Y = self.WIDTH // 2 - self.PLAYER2_TEXT.get_width() // 2, 390
        self.CURSOR_XY = (self.START_X - self.CURSOR_OFFSET, self.START_Y + 10)

    def draw_cursor(self):
        self.SURFACE.blit(self.CURSOR, self.CURSOR_XY)

    def draw_surface(self):
        self.SURFACE.blit(self.BACKGROUND, (0, 0))

        # Display Texts
        self.SURFACE.blit(self.GAME_NAME_TEXT, (self.WIDTH // 2 - self.GAME_NAME_TEXT.get_width() // 2, 100))
        self.SURFACE.blit(self.START_GAME_TEXT, (self.START_X, self.START_Y))
        self.SURFACE.blit(self.HOW_TO_PLAY_TEXT, (self.HOWTO_X, self.HOWTO_Y))
        self.SURFACE.blit(self.CREDITS_TEXT, (self.CREDITS_X, self.CREDITS_Y))
        self.SURFACE.blit(self.PLAYER2_TEXT, (self.PLAYER2_X, self.PLAYER2_Y))

    def move_cursor(self, event):
        if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()
                    
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DOWN:
                if self.CURSOR_STATE == "start":
                    self.CURSOR_XY = (self.HOWTO_X - self.CURSOR_OFFSET, self.HOWTO_Y + 10)
                    self.CURSOR_STATE = "howto"

                elif self.CURSOR_STATE == "howto":
                    self.CURSOR_XY = (self.CREDITS_X - self.CURSOR_OFFSET, self.CREDITS_Y + 10)
                    self.CURSOR_STATE = "credits"

                elif self.CURSOR_STATE == "credits":
                    self.CURSOR_XY = (self.PLAYER2_X - self.CURSOR_OFFSET, self.PLAYER2_Y + 10)
                    self.CURSOR_STATE = "player2"

                elif self.CURSOR_STATE == "player2":
                    self.CURSOR_XY = (self.START_X - self.CURSOR_OFFSET, self.START_Y + 10)
                    self.CURSOR_STATE = "start"

            if event.key == pygame.K_UP:
                if self.CURSOR_STATE == "start":
                    self.CURSOR_XY = (self.PLAYER2_X - self.CURSOR_OFFSET, self.PLAYER2_Y + 10)
                    self.CURSOR_STATE = "player2"

                elif self.CURSOR_STATE == "howto":
                    self.CURSOR_XY = (self.START_X - self.CURSOR_OFFSET, self.START_Y + 10)
                    self.CURSOR_STATE = "start"

                elif self.CURSOR_STATE == "credits":
                    self.CURSOR_XY = (self.HOWTO_X - self.CURSOR_OFFSET, self.HOWTO_Y + 10)
                    self.CURSOR_STATE = "howto"

                elif self.CURSOR_STATE == "player2":
                    self.CURSOR_XY = (self.CREDITS_X - self.CURSOR_OFFSET, self.CREDITS_Y + 10)
                    self.CURSOR_STATE = "credits"

    def check_input(self, event):
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:
                if self.CURSOR_STATE == "start":
                    self.game.reset() 
                    self.game.APP_RUNNING = True
                    self.game.play()
                elif self.CURSOR_STATE == "howto":
                    self.game.CURR_MENU = self.game.HOWTO
                elif self.CURSOR_STATE == "credits":
                    self.game.CURR_MENU = self.game.CREDITS
                elif self.CURSOR_STATE == "player2":
                    self.toggle_player2()
                self.RUNNING = False

    def toggle_player2(self):
        if self.game.PLAYER2_AI:
            self.game.PLAYER2_AI = False
            self.PLAYER2_TEXT = self.MENU_OPTIONS_FONT.render("PLAYER 2: HUMAN", 1, self.WHITE)
        else:
            self.game.PLAYER2_AI = True
            self.PLAYER2_TEXT = self.MENU_OPTIONS_FONT.render("PLAYER 2: AI", 1, self.WHITE)

    def run_menu(self):
        self.RUNNING = True
        clock = pygame.time.Clock()
        while self.RUNNING:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                self.move_cursor(event)
                self.check_input(event)

            self.draw_surface()
            self.draw_cursor()
            pygame.display.update()

        self.RUNNING = False


class HowTo:

    def __init__(self, game):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.game = game
        self.RUNNING = True
        self.WIDTH, self.HEIGHT = 900, 500
        self.SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Spaceship Fighter")

        self.WHITE = (255, 255, 255)
        self.DARK_GRAY = (60, 60, 60)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        self.FPS = 60

        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'menu_bg.png')),
                                                 (self.WIDTH, self.HEIGHT))
        self.RECT_BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "HowToBG.jpeg")), (self.WIDTH - 200,  self.HEIGHT - 160))

        self.W_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "w.png")), (40,  40))
        self.A_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "a.png")), (40, 40))
        self.S_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "s.png")), (40, 40))
        self.D_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "d.png")), (40, 40))

        self.SHIFT_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "shift.png")), (40, 40))

        self.UP_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "up.png")), (40, 40))
        self.DOWN_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "down.png")), (40, 40))
        self.LEFT_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "left.png")), (40, 40))
        self.RIGHT_KEY = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "right.png")), (40, 40))

        self.BORDER = pygame.Rect(self.WIDTH // 2 - 5, 140, 10, self.HEIGHT - 180)

        self.MENU_OPTIONS_FONT = pygame.font.SysFont('comicsans', 40)
        self.HOW_TO_BIG_FONT = pygame.font.SysFont('comicsans', 35)
        self.HOW_TO_SMALL_FONT = pygame.font.SysFont('comicsans', 18)

    def draw_surface(self):
        self.SURFACE.blit(self.BACKGROUND, (0, 0))

        # Draw Graphics
        how_to_text = self.MENU_OPTIONS_FONT.render("How To Play", 1, self.WHITE)
        self.SURFACE.blit(how_to_text, (self.WIDTH // 2 - how_to_text.get_width() // 2 - 10, 40))
        self.SURFACE.blit(self.RECT_BG, (100, 130))
        pygame.draw.rect(self.SURFACE, self.DARK_GRAY, self.BORDER)

        player_1_name_text = self.HOW_TO_BIG_FONT.render("Player 1", 1, self.BLACK)
        player_2_name_text = self.HOW_TO_BIG_FONT.render("Player 2", 1, self.BLACK)

        self.SURFACE.blit(player_1_name_text, (130, 140))
        self.SURFACE.blit(player_2_name_text, (self.BORDER.x + self.BORDER.width + 20, 140))

        self.SURFACE.blit(self.W_KEY, (130, 200))
        self.SURFACE.blit(self.S_KEY, (130, 250))
        self.SURFACE.blit(self.A_KEY, (130, 300))
        self.SURFACE.blit(self.D_KEY, (130, 350))
        self.SURFACE.blit(self.SHIFT_KEY, (130, 400))

        self.SURFACE.blit(self.UP_KEY, (self.BORDER.x + self.BORDER.width + 30, 200))
        self.SURFACE.blit(self.DOWN_KEY, (self.BORDER.x + self.BORDER.width + 30, 250))
        self.SURFACE.blit(self.LEFT_KEY, (self.BORDER.x + self.BORDER.width + 30, 300))
        self.SURFACE.blit(self.RIGHT_KEY, (self.BORDER.x + self.BORDER.width + 30, 350))
        self.SURFACE.blit(self.SHIFT_KEY, (self.BORDER.x + self.BORDER.width + 30, 400))

        w_text = self.HOW_TO_SMALL_FONT.render("Move the Spaceship to Up", 1, self.BLACK)
        a_text = self.HOW_TO_SMALL_FONT.render("Move the Spaceship to Left", 1, self.BLACK)
        s_text = self.HOW_TO_SMALL_FONT.render("Move the Spaceship to Down", 1, self.BLACK)
        d_text = self.HOW_TO_SMALL_FONT.render("Move the Spaceship to Right", 1, self.BLACK)
        shift1_text = self.HOW_TO_SMALL_FONT.render("Fire bullets", 1, self.BLACK)

        self.SURFACE.blit(w_text, (180, 205))
        self.SURFACE.blit(s_text, (180, 255))
        self.SURFACE.blit(a_text, (180, 305))
        self.SURFACE.blit(d_text, (180, 355))
        self.SURFACE.blit(shift1_text, (180, 405))

        self.SURFACE.blit(w_text, (self.BORDER.x + self.BORDER.width + 80, 205))
        self.SURFACE.blit(s_text, (self.BORDER.x + self.BORDER.width + 80, 255))
        self.SURFACE.blit(a_text, (self.BORDER.x + self.BORDER.width + 80, 305))
        self.SURFACE.blit(d_text, (self.BORDER.x + self.BORDER.width + 80, 355))
        self.SURFACE.blit(shift1_text, (self.BORDER.x + self.BORDER.width + 80, 405))

    def check_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.CURR_MENU = self.game.MAIN_MENU
                self.RUNNING = False

    def run_menu(self):
        self.RUNNING = True
        clock = pygame.time.Clock()
        while self.RUNNING:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                self.check_input(event)

            self.draw_surface()
            pygame.display.update()

        self.RUNNING = False


class Credits:

    def __init__(self, game):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()

        self.game = game
        self.RUNNING = True
        self.WIDTH, self.HEIGHT = 900, 500
        self.SURFACE = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.display.set_caption("Spaceship Fighter")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        self.FPS = 60

        self.SMALL_FONT = pygame.font.SysFont('comicsans', 18)

        self.BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'menu_bg.png')),
                                                 (self.WIDTH, self.HEIGHT))
        self.ME_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "me.png")), (350, 250))

        self.MENU_OPTIONS_FONT = pygame.font.SysFont('comicsans', 40)

    def draw_surface(self):
        self.SURFACE.blit(self.BACKGROUND, (0, 0))

        # Display Texts
        credits_text = self.MENU_OPTIONS_FONT.render("Credits", 1, self.WHITE)
        me_text = self.SMALL_FONT.render("Created by Hiroon.", 1, self.WHITE)

        self.SURFACE.blit(credits_text, (self.WIDTH // 2 - credits_text.get_width() // 2 - 10, 40))
        self.SURFACE.blit(self.ME_IMAGE, (self.WIDTH // 2 - self.ME_IMAGE.get_width() // 2, 120))
        self.SURFACE.blit(me_text, (self.WIDTH // 2 - me_text.get_width() // 2 - 10, 370))

    def check_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.CURR_MENU = self.game.MAIN_MENU
                self.RUNNING = False

    def run_menu(self):
        self.RUNNING = True
        clock = pygame.time.Clock()
        while self.RUNNING:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.RUNNING = False
                self.check_input(event)

            self.draw_surface()
            pygame.display.update()

        self.RUNNING = False
