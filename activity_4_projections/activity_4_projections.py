import math
import sys
import pygame


WIDTH, HEIGHT = 800, 600
CUBE_SIZE = 100
CAMERA_DISTANCE = 400

VERTICES = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
]
EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6),
    (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7),
]


def rotate_point(point, angles):
    x, y, z = point
    ax, ay, az = [math.radians(angle) for angle in angles]

    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    return x, y, z


def project(point, mode):
    x, y, z = point
    if mode == 1:
        return x, y
    if mode == 2:
        angle, depth = math.radians(45), 1.0
        return x + z * depth * math.cos(angle), y + z * depth * math.sin(angle)
    if mode == 3:
        angle, depth = math.radians(63.4), 0.5
        return x + z * depth * math.cos(angle), y + z * depth * math.sin(angle)
    denominator = 1 + z / CAMERA_DISTANCE
    if denominator <= 0:
        raise ValueError("Point is on or behind the perspective view plane.")
    return x / denominator, y / denominator


def screen_point(point, mode):
    x, y = project(point, mode)
    return round(WIDTH / 2 + x), round(HEIGHT / 2 - y)


def draw_perspective_guides(screen, font):
    # Parallel world-space lines in the z direction approach one vanishing point.
    for x, y in [(-150, -100), (0, 100), (150, -100)]:
        start = screen_point((x, y, -150), 4)
        end = screen_point((x, y, 3000), 4)
        pygame.draw.line(screen, (170, 80, 170), start, end, 2)
    pygame.draw.circle(screen, (170, 30, 170), (WIDTH // 2, HEIGHT // 2), 5)
    pygame.draw.line(screen, (170, 30, 170),
                     (WIDTH // 2 + 8, HEIGHT // 2 - 8),
                     (WIDTH // 2 + 70, HEIGHT // 2 - 45), 1)
    pygame.display.get_surface().blit(
        font.render("Vanishing point", True, (120, 20, 120)),
        (WIDTH // 2 + 70, HEIGHT // 2 - 58)
    )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Activity 4: 3D Projection Pipeline")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    small_font = pygame.font.Font(None, 22)
    guide_font = pygame.font.Font(None, 22)
    mode = 1
    mode_names = {
        1: "Orthographic",
        2: "Cavalier Oblique",
        3: "Cabinet Oblique",
        4: "One-Point Perspective",
    }
    angles = [20.0, 25.0, 0.0]
    running = True

    while running:
        clock.tick(60)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_x]:
            angles[0] += 1
        if keys[pygame.K_y]:
            angles[1] += 1
        if keys[pygame.K_z]:
            angles[2] += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                    mode = int(event.unicode)

        screen.fill((245, 245, 245))
        screen.blit(font.render("Activity 4: 3D Projection Pipeline", True, (20, 20, 20)),
                    (20, 15))
        screen.blit(font.render(f"Mode: {mode_names[mode]}", True, (20, 20, 20)),
                    (20, 55))
        screen.blit(small_font.render(
            "1 Orthographic   2 Cavalier   3 Cabinet   4 Perspective",
            True, (30, 30, 30)), (20, 95))
        screen.blit(small_font.render(
            "Hold X, Y, or Z to rotate around that axis. Esc: quit.",
            True, (30, 30, 30)), (20, 122))

        if mode == 4:
            draw_perspective_guides(screen, guide_font)
        rotated = [
            tuple(value * CUBE_SIZE for value in rotate_point(vertex, angles))
            for vertex in VERTICES
        ]
        projected = [screen_point(point, mode) for point in rotated]
        for start, end in EDGES:
            pygame.draw.line(screen, (20, 80, 180),
                             projected[start], projected[end], 3)
        for point in projected:
            pygame.draw.circle(screen, (20, 20, 20), point, 4)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    try:
        main()
    except ImportError:
        print("Install pygame with: py -3 -m pip install pygame")
        sys.exit(1)
