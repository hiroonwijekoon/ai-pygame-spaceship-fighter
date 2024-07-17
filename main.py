import pygame

from game import Game

_game = Game()

while _game.APP_RUNNING:
    _game.CURR_MENU.run_menu()
