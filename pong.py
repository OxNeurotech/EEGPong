import pygame
import random

pygame.init()

# Game Constants
WIDTH, HEIGHT = 1280, 960
PADDLE_WIDTH, PADDLE_HEIGHT = 30, 180
CENTRE_WIDTH, CENTRE_HEIGHT = 6, 960
FONT_SIZE = 100

# Colour
CORAL_PINK = (255,128,128)
TEAL_GREEN = (0, 130, 127)

# Load font
font = pygame.font.Font("resources/font.ttf", FONT_SIZE)

# Load sounds
hit_sound = pygame.mixer.Sound("resources/sounds/paddle_hit.wav")
score_sound = pygame.mixer.Sound("resources/sounds/score.wav")
wallhit_sound = pygame.mixer.Sound("resources/sounds/wall_hit.wav")

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
    
    def getPosition(self):
        return self.posx, self.posy


class Ball:
    def __init__(self, posx, posy, radius, speed, colour):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.colour = colour
        self.yFac = self.choose_yFac()
        self.xFac = self.choose_xFac()
        self.ball = pygame.draw.circle(
            screen, self.colour, (self.posx, self.posy), self.radius
        )

    def choose_yFac(self):
        return random.choice([-1, -0.7, -0.5, 0.5, 0.7, 1])
    
    def choose_xFac(self):
        if abs(self.yFac) == 1:
            return 1
        elif abs(self.yFac) == 0.7:
            return 1.23
        else:
            return 1.32

    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.colour, (self.posx, self.posy), self.radius
        )
    
    def update(self, rest=False):
        if not rest:
            self.posx += self.speed * self.xFac
            self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= HEIGHT:
            pygame.mixer.Sound.play(wallhit_sound)
            self.yFac *= -1
        
        if self.posx <= 0 and not rest:
            rest = False
            return 1
        elif self.posx >= WIDTH and not rest:
            rest = False
            return -1
        else:
            return 0
    
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.yFac = self.choose_yFac()
        if self.xFac < 0:
            self.xFac = self.choose_xFac()
        else:
            self.xFac = -self.choose_xFac()
    
    def hit_left(self):
        self.xFac = abs(self.xFac)

    def hit_right(self):
        self.xFac = -abs(self.xFac)

    def getBall(self):
        return self.ball
    
    def getPosition(self):
        return self.posx, self.posy


def main():
    game_on = True
    rest = True

    # Game objects
    playerPaddle = Striker(20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, 8, TEAL_GREEN)
    aiPaddle = Striker(WIDTH - 50, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, 8, TEAL_GREEN)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 15, 3, TEAL_GREEN)
    centre_line = pygame.Rect(WIDTH // 2 - CENTRE_WIDTH // 2, 0, CENTRE_WIDTH, CENTRE_HEIGHT)

    # Initial parameters of the players
    playerScore, aiScore = 0, 0
    player_yFac, ai_yFac = 0, 0

    while game_on:
        screen.fill(CORAL_PINK)
        pygame.draw.rect(screen, TEAL_GREEN, centre_line)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    rest = False
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    player_yFac = -1
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    player_yFac = 1

                # Quit the game if escape is pressed
                if event.key == pygame.K_ESCAPE:
                    game_on = False
            if event.type == pygame.KEYUP:
               if (event.key == pygame.K_w or event.key == pygame.K_s or
               event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                   player_yFac = 0
        
        if aiPaddle.getPosition()[1] + PADDLE_HEIGHT // 2 < ball.getPosition()[1]:
            ai_yFac = 1
        elif aiPaddle.getPosition()[1] + PADDLE_HEIGHT // 2 > ball.getPosition()[1]:
            ai_yFac = -1
        else:
            ai_yFac = 0

        if pygame.Rect.colliderect(ball.getBall(), playerPaddle.getPaddle()):
            pygame.mixer.Sound.play(hit_sound)
            ball.hit_left()
        if pygame.Rect.colliderect(ball.getBall(), aiPaddle.getPaddle()):
            pygame.mixer.Sound.play(hit_sound)
            ball.hit_right()
        
        playerPaddle.update(player_yFac)
        aiPaddle.update(ai_yFac)
        point = ball.update(rest)

        if point == -1:
            playerScore += 1
        elif point == 1:
            aiScore += 1
        
        if point:
            pygame.mixer.Sound.play(score_sound)
            ball.reset()
            rest = True
        
        playerPaddle.display()
        aiPaddle.display()
        ball.display()

        playerPaddle.displayScore(playerScore, 400, 300, TEAL_GREEN)
        aiPaddle.displayScore(aiScore, WIDTH - 400, 300, TEAL_GREEN)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()