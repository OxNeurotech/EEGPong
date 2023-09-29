import pygame
import sys
import random

pygame.init()

# Game Constants
WIDTH, HEIGHT = 1280, 960
FONT_SIZE = 40
PINK = (255,128,128)

# Set up game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EEG Pong")

# Load font
font = pygame.font.Font("../resources/font.ttf", FONT_SIZE)

# Game objects

game_on = True
while game_on:
    screen.fill(PINK)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_on = False
    pygame.display.update()