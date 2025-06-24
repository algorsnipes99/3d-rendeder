from OpenGL.GL import *
from render_matrix import RenderMatrix

class Renderer:
    def __init__(self):
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glLineWidth(1.0)
        glColor3f(1.0, 1.0, 1.0)  # White color for wireframe

    def render(self, render_matrix: RenderMatrix):
        """Render all objects in the matrix as wireframe"""
        glBegin(GL_LINES)
        for i, j in render_matrix.edges:
            v1 = render_matrix.vertices[i]
            v2 = render_matrix.vertices[j]
            glVertex3f(*v1)
            glVertex3f(*v2)
        glEnd()

    def set_projection(self, fov: float, aspect: float, near: float, far: float):
        """Set perspective projection matrix"""
        from OpenGL.GLU import gluPerspective
        gluPerspective(fov, aspect, near, far)

    def set_view(self, x: float, y: float, z: float):
        """Set view transformation matrix"""
        from OpenGL.GLU import gluLookAt
        gluLookAt(x, y, z, 0, 0, 0, 0, 1, 0)
