import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from render_matrix import RenderMatrix
from obj_importer import OBJImporter
from renderer import Renderer
import threading
import time
from queue import Queue

def main():
    pygame.init()
    display = (800, 600)
    
    # Require OpenGL 3.0 core profile
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 0)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK,
                                  pygame.GL_CONTEXT_PROFILE_CORE)
    
    try:
        pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    except pygame.error as e:
        raise RuntimeError(f"OpenGL 3.0 not available: {e}. Please update your graphics drivers.")
    
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
    
    # Initialize physics engine
    from physics import PhysicsEngine
    from physics.rules import GravityRule
    
    physics_engine = PhysicsEngine()
    physics_engine.add_rule(GravityRule(strength=0.005))

    # Physics thread setup
    physics_queue = Queue()
    physics_active = threading.Event()
    physics_active.set()
    
    def physics_worker():
        last_time = time.time()
        while physics_active.is_set():
            current_time = time.time()
            delta = current_time - last_time
            last_time = current_time
            
            physics_engine.process_frame(render_matrix, delta)
            physics_queue.put(True)  # Signal update
            
            # Target 60 physics updates per second
            time.sleep(max(0, 1/60 - (time.time() - current_time)))
    
    physics_thread = threading.Thread(target=physics_worker)
    physics_thread.start()

    # Load test cube
    importer.add_to_render_matrix("./objects/thing1.obj", render_matrix)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                physics_active.clear()
                physics_thread.join()
                pygame.quit()
                return
            control_processor.handle_event(event)
        
        # Update controls before rendering
        movement_controls.update()

        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        # Check for physics updates
        while not physics_queue.empty():
            physics_queue.get()
        
        renderer.render(render_matrix)
        pygame.display.flip()
        clock.tick(120)

if __name__ == "__main__":
    main()
