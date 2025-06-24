import numpy as np
from typing import List, Tuple

class RenderMatrix:
    def __init__(self):
        self.vertices = []  # List of 3D coordinates (x,y,z)
        self.edges = []     # List of vertex index pairs (i,j)
        self.objects = []   # List of object vertex ranges

    def add_object(self, vertices: List[Tuple[float, float, float]], 
                  edges: List[Tuple[int, int]]) -> int:
        """Add a new 3D object to the matrix.
        Returns the object ID for reference."""
        start_idx = len(self.vertices)
        self.vertices.extend(vertices)
        
        # Adjust edge indices to account for existing vertices
        adjusted_edges = [(i+start_idx, j+start_idx) for i,j in edges]
        self.edges.extend(adjusted_edges)
        
        obj_id = len(self.objects)
        self.objects.append((start_idx, len(self.vertices)))
        return obj_id

    def transform(self, matrix: np.ndarray):
        """Apply 4x4 transformation matrix to all vertices"""
        if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
            raise ValueError("Transformation matrix must be 4x4")
            
        # Convert to homogeneous coordinates
        homogenous = np.column_stack([
            np.array(self.vertices),
            np.ones(len(self.vertices))
        ])
        
        # Apply transformation
        transformed = np.dot(homogenous, matrix.T)
        
        # Convert back to 3D coordinates
        self.vertices = [(x,y,z) for x,y,z,_ in transformed]
