import pygame
import random
import math
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FPS = 60
BGCOLOUR = WHITE
AMOUNT_OF_LIVES = 5
ENEMY_SPEED_MULTIPLIER = 1

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
# --- Classes


class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([20, 15])
        self.image.fill(BLUE)
 
        self.rect = self.image.get_rect()

        # set its initial velocity
        x = ENEMY_SPEED_MULTIPLIER
        self.vel_x = random.choice([-3*x, -2*x, 2*x, 3*x])
        self.vel_y = random.choice([-3*x, -2*x, 2*x, 3*x])

    def update(self):
        # move the enemy
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # keep enemy inside the screen
        if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
            self.vel_y = -self.vel_y
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vel_x = -self.vel_x
 
 
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
 
    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
 
        self.rect = self.image.get_rect()

        # max velocity
        self.vel_magnitude = 3

        self.vel_x = 0
        self.vel_y = 0

    def update(self):
        """ movement using the wasd keys """
        # get_pressed -> LIST OF BOOLS
        if pygame.key.get_pressed()[pygame.K_w]:
            self.vel_y = -self.vel_magnitude
        # if key not pressed, don't move
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.vel_y = self.vel_magnitude
        else:
            self.vel_y = 0
        if pygame.key.get_pressed()[pygame.K_a]:
            self.vel_x = -self.vel_magnitude
        # if key not pressed, don't move
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.vel_x = self.vel_magnitude
        else:
            self.vel_x = 0
        # move 
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x
 
 
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """
 
    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """

        super().__init__()
 
        # Bullet
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
 
        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y
 
        # These new variables are simply the starting locations stored as floats
        # so aiming is more accurate
        self.floating_point_x = start_x
        self.floating_point_y = start_y
 
        # Calculate the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff);
 
        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        velocity = 7
        self.change_x = math.cos(angle) * velocity
        self.change_y = math.sin(angle) * velocity
 
    def update(self):
        """ Move the bullet. """
 
        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x
 
        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)
 
        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > SCREEN_WIDTH or self.rect.y < 0 or self.rect.y > SCREEN_HEIGHT:
            self.kill()
 
 
 
# --- Create the window
 
# Initialize Pygame
pygame.init()
 
# Variables
score = 0
lives = AMOUNT_OF_LIVES
level = 1

# Font setup
pygame.font.init()
font = pygame.font.SysFont('Arial',25)

# Set the height and width of the screen
 
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
 
# --- Sprite lists
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each block in the game
block_list = pygame.sprite.Group()
 
# List of each bullet
bullet_list = pygame.sprite.Group()
 
# --- Create the sprites
for i in range(1):
    # This represents a block
    block = Block()
 
    # Set a random location for the block
    block.rect.x = random.randrange(SCREEN_WIDTH - 50)
    block.rect.y = random.randrange(SCREEN_HEIGHT - 50)
 
    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)
 
# Create a red player block
player = Player()
all_sprites_list.add(player)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
player.rect.x = SCREEN_WIDTH / 2
player.rect.y = SCREEN_HEIGHT / 2
 
# -------- Main Program Loop -----------
while not done:
    # --- Game logic
 
    # Call the update() method on all the sprites
    all_sprites_list.update()
 
    # Calculate mechanics for each bullet
    for bullet in bullet_list:
 
        # See if it hit a block
        block_hit_list = pygame.sprite.spritecollide(bullet, block_list, True)
 
        # For each block hit, remove the bullet and add to the score
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            score += 1
 
        # Remove the bullet if it flies up off the screen
        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
 
    # kill block when player hits it
    block_hit_list = pygame.sprite.spritecollide(
        player,
        block_list,
        True
    )

    # spawn new block for each killed
    for hit in block_hit_list:
        lives -= 1

        block = Block()
        # determine initial location
        block.rect.x, block.rect.y = [
        random.randrange(50, SCREEN_WIDTH - 50),
        random.randrange(50, SCREEN_HEIGHT - 50)
        ]

        # add blocks to respective lists
        block_list.add(block)
        all_sprites_list.add(block)

    if not block_list:
        level += 1
        for i in range(pow(2, level)):
            # This represents a block
            block = Block()
    
            # Set a random location for the block
            block.rect.x = random.randrange(SCREEN_WIDTH - 50)
            block.rect.y = random.randrange(SCREEN_HEIGHT - 50)
        
            # Add the block to the list of objects
            block_list.add(block)
            all_sprites_list.add(block)

    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button
 
            # Get the mouse position
            pos = pygame.mouse.get_pos()
 
            mouse_x = pos[0]
            mouse_y = pos[1]

            if level <= 3:    
                # Call the Bullet class to create the projectiles
                bullet = Bullet(player.rect.x, player.rect.y, mouse_x, mouse_y)
 
                # Add the bullet to the lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
            
            elif level > 3 and level <=9:
                # Call the Bullet class to create the projectiles
                bullet_0 = Bullet(player.rect.x, player.rect.y, mouse_x, mouse_y)
                bullet_1 = Bullet(player.rect.x, player.rect.y, mouse_x -10, mouse_y -10)
                bullet_2 = Bullet(player.rect.x, player.rect.y, mouse_x +10, mouse_y +10)
 
                # Add the bullet to the lists
                all_sprites_list.add(bullet_0, bullet_1, bullet_2)
                bullet_list.add(bullet_0, bullet_1, bullet_2)
            
            elif level > 10 and level <=15:
                # Call the Bullet class to create the projectiles
                bullet_0 = Bullet(player.rect.x, player.rect.y, mouse_x, mouse_y)
                bullet_1 = Bullet(player.rect.x, player.rect.y, mouse_x -10, mouse_y -10)
                bullet_2 = Bullet(player.rect.x, player.rect.y, mouse_x +10, mouse_y +10)
                bullet_3 = Bullet(player.rect.x, player.rect.y, -mouse_x, -mouse_y)
 
                # Add the bullet to the lists
                all_sprites_list.add(bullet_0, bullet_1, bullet_2)
                bullet_list.add(bullet_0, bullet_1, bullet_2)




    # --- Draw a frame
 
    # Clear the screen
    screen.fill(BGCOLOUR)
 
    # Draw all the sprites
    all_sprites_list.draw(screen)

    # draw the score and lives
    #render(text, antialias, colour) -> Surface
    score_surface = font.render(f"Score: {score}", False, BLACK)
    lives_surface = font.render(f"Lives: {lives}", False, BLACK)
    level_surface = font.render(f"Level: {level}", False, BLACK)

    # blit(surface, coordinates)
    screen.blit(score_surface, [10, 10])
    screen.blit(lives_surface, [10, 30])
    screen.blit(level_surface, [10, 50])
 
    # Update screen
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(FPS)
 
pygame.quit()
