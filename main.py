import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from render_matrix import RenderMatrix
from obj_importer import OBJImporter
from renderer import Renderer

def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    render_matrix = RenderMatrix()
    importer = OBJImporter()
    renderer = Renderer()

    # Load test cube
    importer.add_to_render_matrix("cube.obj", render_matrix)

    # Simple rotation animation
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    glTranslatef(-0.1, 0, 0)
                elif event.key == pygame.K_RIGHT:
                    glTranslatef(0.1, 0, 0)
                elif event.key == pygame.K_UP:
                    glTranslatef(0, 0.1, 0)
                elif event.key == pygame.K_DOWN:
                    glTranslatef(0, -0.1, 0)

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glRotatef(1, 0, 1, 0)  # Rotate 1 degree per frame around Y axis
        renderer.render(render_matrix)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
