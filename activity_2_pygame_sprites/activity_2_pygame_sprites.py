import random
import sys
try:
    import pygame
except ImportError:
    print("Install pygame with: py -3 -m pip install pygame")
    sys.exit(1)


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (44, 94, 138), (20, 20), 20)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image.fill((210, 55, 55))
        self.rect = self.image.get_rect(
            topleft=(random.randint(20, SCREEN_WIDTH - 50),
                     random.randint(60, SCREEN_HEIGHT - 60)))
        self.speed_x = random.choice([-3, -2, 2, 3])
        self.speed_y = random.choice([-3, -2, 2, 3])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x = -self.speed_x
        if self.rect.top <= 50 or self.rect.bottom >= SCREEN_HEIGHT:
            self.speed_y = -self.speed_y


class ImpactParticle(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 150, 30, 230), (6, 6), 6)
        self.rect = self.image.get_rect(center=position)
        self.velocity = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))
        self.life = 30

    def update(self):
        self.rect.x += round(self.velocity.x)
        self.rect.y += round(self.velocity.y)
        self.life -= 1
        self.image.set_alpha(max(0, int(230 * self.life / 30)))
        if self.life <= 0:
            self.kill()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Activity 2: Sprite System & Collision Arena")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 22)

    player = Player()
    player_group = pygame.sprite.Group(player)
    obstacles = pygame.sprite.Group()
    for _ in range(6):
        obstacles.add(Obstacle())
    particles = pygame.sprite.Group()
    score = 0
    health = 100
    collision_wait = 0
    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        particles.update()
        if health > 0:
            player_group.update()
            obstacles.update()
            score += dt / 1000.0
            collision_wait = max(0, collision_wait - dt)

        # Keep the collided group so every impact can produce particles and respawn.
        hit_any = health > 0 and pygame.sprite.spritecollideany(
            player, obstacles, pygame.sprite.collide_rect
        )
        hits = pygame.sprite.spritecollide(
            player, obstacles, False, pygame.sprite.collide_rect
        ) if hit_any else []
        if hits and collision_wait == 0:
            health = max(0, health - 10)
            collision_wait = 700
            for obstacle in hits:
                for _ in range(8):
                    particles.add(ImpactParticle(obstacle.rect.center))
                obstacle.rect.topleft = (
                    random.randint(20, SCREEN_WIDTH - 50),
                    random.randint(60, SCREEN_HEIGHT - 60),
                )
                obstacle.speed_x = random.choice([-3, -2, 2, 3])
                obstacle.speed_y = random.choice([-3, -2, 2, 3])

        screen.fill((245, 245, 245))
        obstacles.draw(screen)
        particles.draw(screen)
        player_group.draw(screen)

        hud = font.render(f"Score: {int(score)}   Health: {health}", True, (20, 20, 20))
        fps = small_font.render(f"FPS: {clock.get_fps():.1f}", True, (20, 20, 20))
        screen.blit(hud, (15, 12))
        screen.blit(fps, (SCREEN_WIDTH - 110, 16))
        screen.blit(small_font.render("Use arrow keys to move; avoid the red obstacles.",
                                     True, (20, 20, 20)), (15, SCREEN_HEIGHT - 28))
        if health == 0:
            message = font.render("Game over - close the window to exit", True, (180, 20, 20))
            screen.blit(message, message.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        pygame.display.flip()
        if health == 0:
            clock.tick(1)

    pygame.quit()


if __name__ == "__main__":
    main()
