import numpy as np
import numba as nb
import math

class VectorProcessor:
    def __init__(self):
        pass

    @staticmethod
    @nb.njit(fastmath=True)
    def move_vertices(out, vertices, direction, distance):
        """Move vertices along direction vector by distance"""
        nrm = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
        if nrm == 0.0:
            raise ValueError("Zero-length direction vector")
        inv = distance / nrm
        
        # Ensure vertices is 2D array
        if len(vertices.shape) == 1:
            vertices = vertices.reshape(-1, 3)
        if len(out.shape) == 1:
            out = out.reshape(-1, 3)
            
        for i in range(vertices.shape[0]):
            out[i, 0] = vertices[i, 0] + direction[0] * inv
            out[i, 1] = vertices[i, 1] + direction[1] * inv
            out[i, 2] = vertices[i, 2] + direction[2] * inv

    @staticmethod
    @nb.njit(parallel=True, fastmath=True)
    def move_vertices_parallel(out, vertices, direction, distance):
        """Parallel version for large vertex sets"""
        nrm = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)
        if nrm == 0.0:
            raise ValueError("Zero-length direction vector")
        inv = distance / nrm
        
        for i in nb.prange(vertices.shape[0]):
            out[i, 0] = vertices[i, 0] + direction[0] * inv
            out[i, 1] = vertices[i, 1] + direction[1] * inv
            out[i, 2] = vertices[i, 2] + direction[2] * inv

    def apply_force(self, vertices, force_vector, delta_time, parallel=False):
        """Apply force to vertices over time"""
        # Ensure vertices is 2D array
        vertices = np.asarray(vertices)
        if len(vertices.shape) == 1:
            vertices = vertices.reshape(-1, 3)
            
        out = np.empty_like(vertices)
        if parallel and vertices.shape[0] > 1000:  # Threshold for parallel
            self.move_vertices_parallel(out, vertices, force_vector, delta_time)
        else:
            self.move_vertices(out, vertices, force_vector, delta_time)
        return out
