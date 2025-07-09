import numpy as np
from .base_rule import PhysicsRule

class GravityRule(PhysicsRule):
    def __init__(self, strength: float = 0.01):
        self.strength = strength
        self.direction = np.array([0, -1, 0], dtype=np.float64)

    def apply(self, render_matrix, delta_time: float, vector_processor):
        """Apply gravity force to all vertices"""
        vertices = np.array(render_matrix.vertices, dtype=np.float64)
        moved_vertices = vector_processor.apply_force(
            vertices, 
            self.direction * self.strength, 
            delta_time
        )
        render_matrix.vertices = moved_vertices.tolist()
