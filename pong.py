import pygame
import sys
import random

pygame.init()

# Game Constants
WIDTH, HEIGHT = 1280, 960
FONT_SIZE = 100

# Colour
CORAL_PINK = (255,128,128)
TEAL_GREEN = (0, 130, 127)

# Load font
font = pygame.font.Font("resources/font.ttf", FONT_SIZE)

# Used to adjust frame rate
clock = pygame.time.Clock()
FPS = 120

# Set up game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EEG Pong")

class Striker:
    def __init__(self, posx, posy, width, height, speed, colour):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.colour = colour
        self.paddle = pygame.Rect(posx, posy, width, height)
        self.eegpong = pygame.draw.rect(screen, self.colour, self.paddle)

    def display(self):
        self.eegpong = pygame.draw.rect(screen, self.colour, self.paddle)
    
    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac
        if self.posy <= 0:
            self.posy = 0
        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height
        self.paddle = (self.posx, self.posy, self.width, self.height)
    
    def displayScore(self, score, x, y, colour):
        text = font.render(f"{score}", True, colour)
        textPaddle = text.get_rect()
        textPaddle.center = (x, y)
        screen.blit(text, textPaddle)

    def getPaddle(self):
        return self.paddle
    

class Ball:
    def __init__(self, posx, posy, radius, speed, colour):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.colour = colour
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            screen, self.colour, (self.posx, self.posy), self.radius
        )
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.colour, (self.posx, self.posy), self.radius
        )
    
    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1
        
        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
    
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1
    
    def hit(self):
        self.xFac *= -1

    def getBall(self):
        return self.ball


def main():
    game_on = True

    # Game objects
    paddle1 = Striker(20, HEIGHT // 2, 10, 100, 10, TEAL_GREEN)
    paddle2 = Striker(WIDTH - 30, HEIGHT // 2, WIDTH / 128, HEIGHT / 9.6, 10, TEAL_GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 15, 3, TEAL_GREEN)
    
    paddleList = [paddle1, paddle2]

    # Initial parameters of the players
    paddle1Score, paddle2Score = 0, 0
    paddle1yFac, paddle2yFac = 0, 0

    while game_on:
        screen.fill(CORAL_PINK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle1yFac = -1
                if event.key == pygame.K_s:
                    paddle1yFac = 1
                if event.key == pygame.K_UP:
                    paddle2yFac = -1
                if event.key == pygame.K_DOWN:
                    paddle2yFac = 1
                # Quit the game if escape is pressed
                if event.key == pygame.K_ESCAPE:
                    game_on = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle1yFac = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle2yFac = 0
        
        for paddle in paddleList:
            if pygame.Rect.colliderect(ball.getBall(), paddle.getPaddle()):
                ball.hit()
        
        paddle1.update(paddle1yFac)
        paddle2.update(paddle2yFac)
        point = ball.update()

        if point == -1:
            paddle1Score += 1
        elif point == 1:
            paddle2Score += 1
        
        if point:
            ball.reset()
        
        paddle1.display()
        paddle2.display()
        ball.display()

        paddle1.displayScore(paddle1Score, 400, 300, TEAL_GREEN)
        paddle2.displayScore(paddle2Score, WIDTH - 400, 300, TEAL_GREEN)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()