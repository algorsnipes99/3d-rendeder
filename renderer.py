from OpenGL.GL import *
import numpy as np
from render_matrix import RenderMatrix

class Renderer:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glLineWidth(1.0)
        glColor3f(1.0, 1.0, 1.0)  # White color for wireframe
        self.vbo = None
        self.ebo = None
        self.current_hash = None
        try:
            glGenBuffers(1)  # Test if function exists
        except Exception as e:
            raise RuntimeError("OpenGL 3.0+ required - glGenBuffers not available") from e

    def _setup_buffers(self, render_matrix):
        """Initialize or update VBO and EBO"""
        matrix_hash = hash((tuple(map(tuple, render_matrix.vertices)), 
                          tuple(render_matrix.edges)))
        
        if matrix_hash != self.current_hash:
            # Clear old buffers if they exist
            if self.vbo is not None:
                glDeleteBuffers(1, [self.vbo])
                glDeleteBuffers(1, [self.ebo])
            
            # Create new buffers
            vertices = np.array(render_matrix.vertices, dtype=np.float32)
            edges = np.array(render_matrix.edges, dtype=np.uint32).flatten()
            
            self.vbo = glGenBuffers(1)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
            
            self.ebo = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, edges.nbytes, edges, GL_STATIC_DRAW)
            
            self.current_hash = matrix_hash

    def render(self, render_matrix: RenderMatrix):
        """Render all objects using VBOs"""
        self._setup_buffers(render_matrix)
        
        glEnableClientState(GL_VERTEX_ARRAY)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glVertexPointer(3, GL_FLOAT, 0, None)
        
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glDrawElements(GL_LINES, len(render_matrix.edges)*2, GL_UNSIGNED_INT, None)
        
        glDisableClientState(GL_VERTEX_ARRAY)

    def set_projection(self, fov: float, aspect: float, near: float, far: float):
        """Set perspective projection matrix"""
        from OpenGL.GLU import gluPerspective
        gluPerspective(fov, aspect, near, far)

    def set_view(self, x: float, y: float, z: float):
        """Set view transformation matrix"""
        from OpenGL.GLU import gluLookAt
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)
