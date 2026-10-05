import sys
import math

try:
    import pygame
    from OpenGL.GL import *
    from OpenGL.GLU import gluPerspective
except ImportError:
    print("Install pygame and PyOpenGL with: py -3 -m pip install pygame PyOpenGL")
    sys.exit(1)


vertices = [
    (1, -1, -1), (1, 1, -1), (-1, 1, -1), (-1, -1, -1),
    (1, -1, 1), (1, 1, 1), (-1, -1, 1), (-1, 1, 1)
]
faces = [
    (0, 1, 2, 3), (3, 2, 6, 7), (7, 6, 5, 4),
    (4, 5, 1, 0), (1, 5, 6, 2), (4, 0, 3, 7)
]
vertex_colors = [
    (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0),
    (1, 0, 1), (0, 1, 1), (1, 1, 1), (0.5, 0.5, 0.5)
]


def draw_cube():
    glBegin(GL_QUADS)
    for face in faces:
        for vertex_index in face:
            glColor3fv(vertex_colors[vertex_index])
            glVertex3fv(vertices[vertex_index])
    glEnd()


def draw_arm(angle):
    glPushMatrix()
    glTranslatef(-2.4, -0.2, 0)
    glRotatef(angle, 0, 0, 1)

    glPushMatrix()
    glTranslatef(0.9, 0, 0)
    glScalef(0.9, 0.22, 0.22)
    draw_cube()
    glPopMatrix()

    glTranslatef(1.8, 0, 0)
    glRotatef(30 + 25 * math.sin(math.radians(angle * 0.04)), 0, 0, 1)
    glPushMatrix()
    glTranslatef(0.65, 0, 0)
    glScalef(0.65, 0.16, 0.16)
    draw_cube()
    glPopMatrix()
    glPopMatrix()


def draw_transparent_quads(alpha):
    glDepthMask(GL_FALSE)
    glBegin(GL_QUADS)
    glColor4f(1.0, 0.2, 0.2, alpha)
    glVertex3f(0.2, -1.2, -0.5)
    glVertex3f(2.5, -1.2, -0.5)
    glVertex3f(2.5, 1.2, -0.5)
    glVertex3f(0.2, 1.2, -0.5)

    glColor4f(0.2, 0.3, 1.0, alpha)
    glVertex3f(0.8, -1.2, 0.5)
    glVertex3f(2.8, -1.2, 0.5)
    glVertex3f(2.8, 1.2, 0.5)
    glVertex3f(0.8, 1.2, 0.5)
    glEnd()
    glDepthMask(GL_TRUE)


def main():
    pygame.init()
    width, height = 800, 600
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 24)
    pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)
    pygame.display.set_caption("Activity 5: PyOpenGL (B: toggle transparency, Esc: quit)")

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClearColor(0.08, 0.08, 0.08, 1)

    clock = pygame.time.Clock()
    angle = 0.0
    blend = True
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_b:
                    blend = not blend

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0, 0, -8)

        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        draw_cube()
        glPopMatrix()

        draw_arm(angle)
        draw_transparent_quads(0.5 if blend else 1.0)

        pygame.display.flip()
        angle = (angle + 60 * dt) % 360

    pygame.quit()


if __name__ == "__main__":
    main()
