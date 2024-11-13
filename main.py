# A6: Extending the Avoider Game
# By Yejin Jeon, Chanhee Yoo

import pygame, sys, math, random, time

# Test if two sprite masks overlap
def pixel_collision(mask1, rect1, mask2, rect2):
    offset_x = rect2[0] - rect1[0]
    offset_y = rect2[1] - rect1[1]
    # See if the two masks at the offset are overlapping.
    overlap = mask1.overlap(mask2, (offset_x, offset_y))
    if overlap:
        return True
    else:
        return False

# A basic Sprite class that can draw itself, move, and test collisions. Basically the same as
# the Character example from class.
class Sprite:
    def __init__(self, image):
        self.image = image
        self.rectangle = image.get_rect()
        self.mask = pygame.mask.from_surface(image)

    def draw(self, screen):
        screen.blit(self.image, self.rectangle)

    def is_colliding(self, other_sprite):
        return pixel_collision(self.mask, self.rectangle, other_sprite.mask, other_sprite.rectangle)

class Player(Sprite):
    def __init__(self, image):
        super().__init__(image)

    def set_position(self, new_position):
        self.rectangle.center = new_position

# Enemy class with random starting position, speed, movement, and bounce handling
class Enemy(Sprite):
    def __init__(self, image, width, height):
        super().__init__(image)
        self.rectangle = image.get_rect()
        self.Speed()
        # Initialize enemy at a random position within screen bounds
        self.rectangle.center = (random.randint(0, width), random.randint(0,height))

    def Speed(self):
        self.speed = [random.randint(-6, 6), random.randint(-6, 6)]

    def move(self):
        self.rectangle.move_ip(*self.speed)

    def bounce(self, width, height):
        print("need to implement bounce!")
        if self.rectangle.left <= 0 or self.rectangle.right >= width:
            self.speed[0] = -self.speed[0]
        if self.rectangle.top <= 0 or self.rectangle.bottom >= height:
            self.speed[1] = -self.speed[1]

class PlatformEnemy(Enemy):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.speed[1] = 0

# PowerUp class with a fixed position, collision detection, and drawing capabilities
class PowerUp(Sprite):
    def __init__(self, image, width, height):
        super().__init__(image)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, width), random.randint(0, height))

class RotatingPowerUp(PowerUp):
    def __init__(self, image, width, height):
        super().__init__(image, width, height)
        self.angle = 0 
        self.original_image = self.image
        
    def draw(self, screen):
        self.angle += 5 
        rotated_image = pygame.transform.rotate(self.original_image, self.angle)
        self.image = rotated_image
        
        current_center = self.rect.center
        self.rect = self.image.get_rect(center = current_center)
        
        self.mask = pygame.mask.from_surface(self.image)
        
        super().draw(screen)


# Shield class for temporary protection, granting invincibility to the player upon collection
class Shield(Sprite):
    def __init__(self, image, width, height):
        self.image = image
        self.mask = pygame.mask.from_surface(image)
        self.rectangle = image.get_rect()
        # Random initial position on screen
        self.rectangle.center = (random.randint(0, width), random.randint(0, height))


# StartScreen class to display a "Game Start" message at the beginning
class StartScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('monospace', 50)
        self.message = self.font.render("Game Start!", True, (255, 255, 255))

    def display(self):
        # Displays the start message on the screen
        self.screen.fill((0, 0, 0))
        text_rect = self.message.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(self.message, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)


# GameOverScreen class to display a "Game Over" message at the end
class GameOverScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('monospace', 50)
        self.message = self.font.render("Game Over", True, (255, 0, 0))

    def display(self):
        # Displays the game over message on the screen
        self.screen.fill((0, 0, 0))
        text_rect = self.message.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(self.message, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)


# StageScreen class to display messages upon completing each stage
class StageScreen:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont('monospace', 36)

    def display(self, message):
        # Displays the stage completion message
        self.screen.fill((0, 0, 0))
        text_surface = self.font.render(message, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)


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

        # Power-up collisions
        for powerup in powerups:
            if powerup.is_colliding(player_sprite):
                life += 1

        # Check for player collisions with shields
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


        # Occasionally spawn new power-up
        if random.randint(0, 150) < 2:
            powerups.append(PowerUp(powerup_image, width, height))

        if random.randint(0, 300) < 1:  # Lower chance to spawn rotating power-up
            powerups.append(RotatingPowerUp(powerup_image, width, height))

        if random.randint(0, 300) < 1: #0.33 probability
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