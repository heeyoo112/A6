# A6: Extending the Avoider Game
# By Yejin Jeon, Chanhee Yoo.

import pygame, sys, math, random, time


# Function to test if two sprite masks overlap, indicating a collision
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # Check if the two masks overlap with the calculated offset
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    if overlap:
        return True
    else:
        return False


# Basic Sprite class for drawable game objects with movement and collision handling
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)  # Mask for precise collision detection

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)  # Draw sprite to screen

    # Check for collision with another sprite
    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)


# Player class, derived from Sprite, with position-setting functionality
class Player(Sprite):
    def __init__(self, image):
        super().__init__(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position  # Update player's position


# Enemy class inherits the initial function from Sprite class.
class Enemy(Sprite):
    def __init__(self, image, width, height):
        super().__init__(image)
        self.Speed()
        # Initialize enemy at a random position within screen bounds
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))

    #sets random speed for enemies.
    def Speed(self):
        self.speed = [random.randint(-6, 6), random.randint(-6, 6)]

    def move(self):
        self.rectangle.move_ip(*self.speed)  # Move enemy based on speed

    def bounce(self, width, height):
        # Reverse direction if hitting screen boundaries (bounce effect)
        if self.rectangle.left <= 0 or self.rectangle.right >= width:
            self.speed[0] = -self.speed[0]
        if self.rectangle.top <= 0 or self.rectangle.bottom >= height:
            self.speed[1] = -self.speed[1]


# PowerUp class inherits functions from its parent class, Sprite class.
class PowerUp(Sprite):
    def __init__(self, image, width, height):
        super().__init__(image)
        # Set a random initial position each time a PowerUp is created
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))


# PlatformEnemy class, a type of Enemy that only moves horizontally
class PlatformEnemy(Enemy):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.speed[1] = 0  # Set vertical speed to 0 for horizontal movement only

        # Set horizontal speed (vx) to a random non-zero value to ensure movement
        self.speed[0] = random.choice([-5, -4, -3, 3, 4, 5])


# RotatingPowerUp class for rotating collectibles that can be drawn on screen
class RotatingPowerUp(PowerUp):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.angle = 0  # Initialize rotation angle
        self.original_image = self.image  # Store original image for rotation

    def draw(self, screen):
        # Rotate image by updating angle and reset mask and rectangle for new position
        self.angle += 5
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = rotated_image

        # Maintain current center while updating rotated image rect
        current_center = self.rectangle.center
        self.rectangle = self.image.get_rect(center=current_center)

        # Update mask for accurate collision after rotation
        self.mask = pygame.mask.from_surface(self.image)

        super().draw(screen)  # Draw the rotated image to the screen


# Shield class grants temporary protection to the player when collected
class Shield(Sprite):
    def __init__(self, image, width, height):
        super().__init__(image)
        # Position shield at a random location on the screen
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))


# StartScreen class for displaying a "Game Start" message
class StartScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('monospace', 50)
        self.message = self.font.render("Game Start!", True, (255, 255, 255))

    def display(self):
        # Displays the start message in the center of the screen
        self.screen.fill((0, 0, 0))
        text_rect = self.message.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(self.message, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Pause for 2 seconds before proceeding


# GameOverScreen class for displaying a "Game Over" message
class GameOverScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('monospace', 50)
        self.message = self.font.render("Game Over", True, (255, 0, 0))

    def display(self):
        # Displays the game over message in the center of the screen
        self.screen.fill((0, 0, 0))
        text_rect = self.message.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(self.message, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Pause for 2 seconds before restarting or exiting


# StageScreen class for displaying stage completion messages.
# Since this class is a separated class that is only for starting/ending screen, it does not inherit anything from Sprite class.
class StageScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('monospace', 36)

    def display(self, message):
        # Displays a custom stage message in the center of the screen
        self.screen.fill((0, 0, 0))
        text_surface = self.font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Pause for 2 seconds before continuing to the next stage


# Main game function
def main():
    pygame.init()
    width, height = 700, 700
    screen = pygame.display.set_mode((width, height))

    # Initialize screens
    start_screen = StartScreen(screen, width, height)
    game_over_screen = GameOverScreen(screen, width, height)
    stage_screen = StageScreen(screen, width, height)

    # Display Start Screen
    start_screen.display()

    # Game variables and objects
    myfont = pygame.font.SysFont('monospace', 24)

    #gets images that are necessary for the gameplay.
    player_image = pygame.image.load("jerry.png").convert_alpha()
    player_image = pygame.transform.smoothscale(player_image, (70, 70))

    cat_image = pygame.image.load("tom.png").convert_alpha()
    cat_image = pygame.transform.smoothscale(cat_image, (70, 70))

    dog_image = pygame.image.load("dog.png").convert_alpha()
    dog_image = pygame.transform.smoothscale(dog_image, (70, 70))

    powerup_image = pygame.image.load("cheese.png").convert_alpha()
    powerup_image = pygame.transform.smoothscale(powerup_image, (60, 60))

    star_image = pygame.image.load("star.png").convert_alpha()
    star_image = pygame.transform.smoothscale(star_image, (60, 60))

    platform_enemy_image = pygame.image.load("duck.png").convert_alpha()
    platform_enemy_image = pygame.transform.smoothscale(platform_enemy_image, (70, 70))


    player_sprite = Player(player_image)
    life = 3
    has_shield = False  # Track if player has an active shield

    #produce enemies in range of 5 for normal enemies, and range 3 for platform enemies.
    enemy_sprites = [Enemy(random.choice([cat_image, dog_image]), width, height) for _ in range(5)]
    platform_enemies = [PlatformEnemy(platform_enemy_image, width, height) for _ in range(3)]

    powerups = []
    shields = []

    # Stage and timing variables
    start_time = time.time()
    stage_duration = 10  # 10 seconds per stage
    current_stage = 1

    # Main game loop
    is_playing = True
    while is_playing:
        elapsed_time = time.time() - start_time

        # Check if stage time has passed
        if elapsed_time >= current_stage * stage_duration:
            stage_screen.display(f"Stage {current_stage} complete! Continue!")
            current_stage += 1

        # Check for game over
        if life <= 0:
            is_playing = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_playing = False

        # Player movement
        pos = pygame.mouse.get_pos()
        player_sprite.set_position(pos)

        # Enemy collisions
        for enemy in enemy_sprites:
            if enemy.is_colliding(player_sprite):
                if has_shield:
                    # Use up shield on first collision
                    has_shield = False
                else:
                    life -= 0.1  # Reduce life if no shield

        # Check Power-up collisions
        for powerup in powerups:
            if powerup.is_colliding(player_sprite):
                life += 1

        # Shield collisions
        for shield in shields:
            if shield.is_colliding(player_sprite):
                has_shield = True  # Activate shield on collision
                shields.remove(shield)  # Remove shield after collection

        # Remove collected power-ups
        powerups = [p for p in powerups if not p.is_colliding(player_sprite)]

        # Move and bounce enemies
        for enemy in enemy_sprites:
            enemy.move()
            enemy.bounce(width, height)

            # Move and bounce platform enemies
            for platform_enemy in platform_enemies:
                platform_enemy.move()
                platform_enemy.bounce(width, height)


        # Occasionally spawn a new power-up
        if random.randint(0, 150) < 2:
            powerups.append(PowerUp(powerup_image, width, height))

        if random.randint(0, 300) < 1:  # Lower chance to spawn rotating power-up
            powerups.append(RotatingPowerUp(powerup_image, width, height))

        # Occasionally spawn new shield
        if random.randint(0, 300) < 1:
            shields.append(Shield(star_image, width, height))

        # Render the game
        screen.fill((0, 100, 50))
        player_sprite.draw(screen)

        # Draw all enemies and platform enemies
        for enemy in enemy_sprites:
            enemy.draw(screen)
        for platform_enemy in platform_enemies:
            platform_enemy.draw(screen)

        # Draw all power-ups and shields
        for powerup in powerups:
            powerup.draw(screen)
        for shield in shields:
            shield.draw(screen)

        # Display player life
        life_text = f"Life: {life:.1f}"
        life_banner = myfont.render(life_text, True, (255, 255, 0))
        screen.blit(life_banner, (20, 20))

        pygame.display.update()
        pygame.time.wait(20)

    # Display Game Over Screen
    game_over_screen.display()

    pygame.quit()
    sys.exit()


# Run the game
if __name__ == "__main__":
    main()
