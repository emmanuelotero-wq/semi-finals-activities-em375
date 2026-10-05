import math
import pygame


WIDTH, HEIGHT = 800, 600
FPS = 60


def lerp_point(start, end, t):
    return (start[0] + (end[0] - start[0]) * t,
            start[1] + (end[1] - start[1]) * t)


def ease_in_out(t):
    return t * t * (3 - 2 * t)


def spline_point(points, t):
    position = (t % 1.0) * len(points)
    segment = int(position)
    local_t = position - segment
    p0 = points[(segment - 1) % len(points)]
    p1 = points[segment % len(points)]
    p2 = points[(segment + 1) % len(points)]
    p3 = points[(segment + 2) % len(points)]
    t2 = local_t * local_t
    t3 = t2 * local_t
    return tuple(0.5 * (
        2 * p1[i] + (-p0[i] + p2[i]) * local_t
        + (2 * p0[i] - 5 * p1[i] + 4 * p2[i] - p3[i]) * t2
        + (-p0[i] + 3 * p1[i] - 3 * p2[i] + p3[i]) * t3
    ) for i in range(2))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Activity 1: 2D Animation, Tweening & Morphing Engine")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    small_font = pygame.font.Font(None, 22)

    mode = 1
    elapsed = 0.0
    path = [(80, 170), (220, 100), (360, 210), (500, 110), (690, 190)]
    triangle = [(190, 190), (300, 350), (240, 350), (210, 350)]
    rectangle = [(150, 170), (320, 170), (320, 350), (150, 350)]
    ball_x, ball_y = 600.0, 100.0
    ball_vx, ball_vy = 150.0, 0.0
    gravity = 500.0
    restitution = 0.78
    floor_y = 500
    sprite_image = pygame.Surface((36, 36), pygame.SRCALPHA)
    pygame.draw.circle(sprite_image, (50, 120, 220), (18, 18), 18)
    sprite_rect = sprite_image.get_rect()
    running = True

    while running:
        dt = min(clock.tick(FPS) / 1000.0, 0.05)
        elapsed += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    mode = int(event.unicode)

        screen.fill((245, 245, 245))
        title = font.render("Activity 1: Animation, Tweening & Morphing", True, (20, 20, 20))
        screen.blit(title, (20, 15))
        screen.blit(small_font.render(
            "Press 1: Tweening   2: Morphing   3: Dynamics   Esc: Quit",
            True, (30, 30, 30)), (20, 48))

        if mode == 1:
            screen.blit(font.render("1.1 Tweening along a multi-point spline", True, (20, 20, 20)),
                        (20, 90))
            pygame.draw.lines(screen, (120, 120, 120), False, path, 2)
            for point in path:
                pygame.draw.circle(screen, (70, 70, 70), point, 5)
            t = (elapsed % 6.0) / 6.0
            x, y = spline_point(path, ease_in_out(t))
            sprite_rect.center = round(x), round(y)
            screen.blit(sprite_image, sprite_rect)
            screen.blit(small_font.render("Elapsed time: 6-second loop at 60 FPS",
                                          True, (30, 30, 30)), (20, 550))

        elif mode == 2:
            screen.blit(font.render("1.2 Triangle to rectangle morph", True, (20, 20, 20)),
                        (20, 90))
            t = (math.sin(elapsed * 1.1) + 1) / 2
            t = ease_in_out(t)
            points = [lerp_point(a, b, t) for a, b in zip(triangle, rectangle)]
            pygame.draw.polygon(screen, (100, 190, 130), points)
            pygame.draw.polygon(screen, (20, 70, 30), points, 3)
            screen.blit(small_font.render(
                "The triangle base has a subdivided edge so both shapes have four vertices.",
                True, (30, 30, 30)), (20, 550))

        else:
            ball_vy += gravity * dt
            ball_x += ball_vx * dt
            ball_y += ball_vy * dt
            if ball_x < 20 or ball_x > WIDTH - 20:
                ball_x = max(20, min(WIDTH - 20, ball_x))
                ball_vx = -ball_vx * restitution
            if ball_y + 20 >= floor_y:
                ball_y = floor_y - 20
                ball_vy = -ball_vy * restitution
                ball_vx *= 0.98
            screen.blit(font.render("1.3 Bouncing ball dynamics", True, (20, 20, 20)),
                        (20, 90))
            pygame.draw.line(screen, (50, 50, 50), (0, floor_y), (WIDTH, floor_y), 2)
            pygame.draw.circle(screen, (230, 100, 50),
                               (round(ball_x), round(ball_y)), 20)
            screen.blit(small_font.render(
                f"Position: ({ball_x:.1f}, {ball_y:.1f})  "
                f"Velocity: ({ball_vx:.1f}, {ball_vy:.1f})  "
                f"Gravity: {gravity:.0f} px/s^2  Restitution: {restitution}",
                True, (30, 30, 30)), (20, 550))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
