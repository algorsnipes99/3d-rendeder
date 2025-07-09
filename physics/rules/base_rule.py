from abc import ABC, abstractmethod
from physics.vector_processor import VectorProcessor
from render_matrix import RenderMatrix

class PhysicsRule(ABC):
    @abstractmethod
    def apply(self, render_matrix: RenderMatrix, delta_time: float, vector_processor: VectorProcessor):
        """Apply this physics rule to the render matrix"""
        pass
