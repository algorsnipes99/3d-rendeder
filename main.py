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
    # Initialize control system
    from controls.control_processor import ControlProcessor
    from controls.basic_movement import BasicMovementControls
    
    control_processor = ControlProcessor()
    movement_controls = BasicMovementControls()
    control_processor.register_control(movement_controls)
    
    # Set initial view
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    movement_controls.update()

    render_matrix = RenderMatrix()
    importer = OBJImporter()
    renderer = Renderer()

    # Load test cube
    importer.add_to_render_matrix("thing.obj", render_matrix)

    # Simple rotation animation
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            control_processor.handle_event(event)
        
        # Update controls before rendering
        movement_controls.update()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        renderer.render(render_matrix)
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
