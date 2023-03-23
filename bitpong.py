import pygame

# initialize pygame
pygame.init()

# set the screen dimensions
screen_width = 800
screen_height = 600

# create the screen
screen = pygame.display.set_mode((screen_width, screen_height))

# load the background image
background = pygame.image.load("bitpong.png")

# load the paddle hit sound effect
paddle_hit_sound = pygame.mixer.Sound("effect.wav")

# load the bitcoin image and resize it
bitcoin_img = pygame.image.load("bitcoin.png")
bitcoin_img = pygame.transform.scale(bitcoin_img, (49, 49))

# define the ball class
class Ball:
    def __init__(self):
        self.image = bitcoin_img
        self.rect = self.image.get_rect()
        self.rect.x = screen_width - 50
        self.rect.y = screen_height - 50
        self.speed_x = .51  # set a slower horizontal speed
        self.speed_y = .51  # set a slower vertical speed

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.x <= 0 or self.rect.x >= screen_width - self.rect.width:
            self.speed_x *= -1
        if self.rect.y <= 0 or self.rect.y >= screen_height - self.rect.height:
            self.speed_y *= -1

    def draw(self):
        screen.blit(self.image, self.rect)

# Set up the score
player_score = 69
computer_score = 69
font = pygame.font.Font(None, 36)

# define the paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 145)
        self.speed = 30

    def update(self, direction):
        if direction == "up":
            self.rect.y -= self.speed
        elif direction == "down":
            self.rect.y += self.speed
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > screen_height - self.rect.height:
            self.rect.y = screen_height - self.rect.height

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

# create the ball object
ball = Ball()

# create the paddles
player_paddle = Paddle(50, 250)
computer_paddle = Paddle(screen_width - 50, 250)

# set the initial scores
player_score = -1
computer_score = 0

# set the game loop
running = True
while running:
# handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# get the current position of the mouse cursor
    mouse_pos = pygame.mouse.get_pos()

# update the player paddle
    player_paddle.rect.y = mouse_pos[1]

# update the ball
    ball.update()

# update the computer paddle
    if ball.speed_x > 0:
        if ball.rect.centery < computer_paddle.rect.centery:
            computer_paddle.update("up")
        elif ball.rect.centery > computer_paddle.rect.centery:
            computer_paddle.update("down")

# check for collision with the walls
    if ball.rect.right >= screen_width:
        player_score += 1
    elif ball.rect.left <= 0:
        computer_score += 1

# set the volume of the paddle hit sound effect
    paddle_hit_sound.set_volume(0.039)
    
# Check if the ball hit the player's paddle
    if (ball.rect.bottom >= player_paddle.rect.top and 
       ball.rect.top <= player_paddle.rect.bottom and 
       ball.rect.right >= player_paddle.rect.left and 
       ball.rect.left <= player_paddle.rect.right):
    
       paddle_hit_sound.set_volume(0.02) # adjust the volume level to half
       paddle_hit_sound.play()
       ball.velocity_y = 1
# check for collision with the paddles
    if ball.rect.colliderect(player_paddle.rect) or ball.rect.colliderect(computer_paddle.rect):
        ball.speed_x *= 1
    if ball.rect.colliderect(player_paddle.rect):
        ball.speed_x *= -1
        paddle_hit_sound.play()
    elif ball.rect.colliderect(computer_paddle.rect):
          ball.speed_x *= -1
          paddle_hit_sound.play()


# draw the screen
    screen.fill((0, 0, 0))
    ball.draw()
    player_paddle.draw()
    computer_paddle.draw()
    score_text = font.render(f"{player_score} - {computer_score}", True, (255, 255, 255))
    screen.blit(score_text, ((screen_width - score_text.get_width()) / 2, 10))
    player_score_text = font.render(f"Maxi: {player_score}", True, (255, 255, 255))
    screen.blit(player_score_text, (20, 20))
    computer_score_text = font.render(f"Satoshi: {computer_score}", True, (255, 255, 255))
    screen.blit(computer_score_text, (screen_width - computer_score_text.get_width() - 20, 20))
    screen.blit(background, (330, 570))
    pygame.display.flip()
    pygame.display.update()
# quit pygame
pygame.quit()