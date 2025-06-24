from typing import List, Tuple
from render_matrix import RenderMatrix

class OBJImporter:
    def parse(self, filepath: str) -> Tuple[List[Tuple[float, float, float]], 
                                   List[Tuple[int, int]]]:
        """Parse OBJ file and return vertices and edges"""
        vertices = []
        faces = []
        
        with open(filepath, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    # Parse vertex: v x y z
                    parts = line.strip().split()
                    vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
                elif line.startswith('f '):
                    # Parse face: f v1 v2 v3 ...
                    parts = line.strip().split()[1:]
                    face_verts = [int(p.split('/')[0]) - 1 for p in parts]  # Convert to 0-based
                    faces.append(face_verts)
        
        # Convert faces to edges (assume convex polygons)
        edges = set()
        for face in faces:
            for i in range(len(face)):
                j = (i + 1) % len(face)
                edge = tuple(sorted((face[i], face[j])))
                edges.add(edge)
                
        return vertices, list(edges)
    
    def add_to_render_matrix(self, filepath: str, render_matrix: RenderMatrix) -> int:
        """Parse OBJ file and add to render matrix"""
        vertices, edges = self.parse(filepath)
        return render_matrix.add_object(vertices, edges)
