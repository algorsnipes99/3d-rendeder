import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from .base_controls import BaseControls

class BasicMovementControls(BaseControls):
    """Handles basic camera movement controls"""
    
    def __init__(self):
        self.camera_pos = [0, 0, -5]
        self.camera_rot = [0, 0]
        self.zoom = 5.0
        self.is_dragging = False
        self.last_mouse_pos = (0, 0)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.camera_pos[0] -= 0.1
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.camera_pos[0] += 0.1
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.camera_pos[1] += 0.1
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.camera_pos[1] -= 0.1
            elif event.key == pygame.K_r:  # Reset view
                self.reset_view()
            elif event.key == pygame.K_q:  # Move backward
                self.camera_pos[2] += 0.1
            elif event.key == pygame.K_e:  # Move forward
                self.camera_pos[2] -= 0.1
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.is_dragging = True
                self.last_mouse_pos = event.pos
            elif event.button == 4:  # Mouse wheel up
                self.zoom = max(1.0, self.zoom - 0.5)
            elif event.button == 5:  # Mouse wheel down
                self.zoom += 0.5
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.is_dragging = False
                
        elif event.type == pygame.MOUSEMOTION:
            if self.is_dragging:
                x, y = event.pos
                dx, dy = x - self.last_mouse_pos[0], y - self.last_mouse_pos[1]
                self.camera_rot[0] += dy * 0.5
                self.camera_rot[1] += dx * 0.5
                self.last_mouse_pos = (x, y)
    
    def update(self):
        """Update view matrix - to be called before rendering"""
        glLoadIdentity()
        glTranslatef(*self.camera_pos)
        glRotatef(self.camera_rot[0], 1, 0, 0)  # Pitch (up/down)
        glRotatef(self.camera_rot[1], 0, 1, 0)  # Yaw (left/right)
        glTranslatef(0, 0, -self.zoom)
    
    def reset_view(self):
        """Reset camera to default position"""
        self.camera_pos = [0, 0, -5]
        self.camera_rot = [0, 0]
        self.zoom = 5.0
