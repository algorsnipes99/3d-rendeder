from typing import List
from .vector_processor import VectorProcessor
from .rules.base_rule import PhysicsRule

class PhysicsEngine:
    def __init__(self):
        self.vector_processor = VectorProcessor()
        self.rules: List[PhysicsRule] = []

    def add_rule(self, rule: PhysicsRule):
        """Add a physics rule to be processed each frame"""
        self.rules.append(rule)

    def process_frame(self, render_matrix, delta_time: float):
        """Apply all physics rules to the render matrix"""
        for rule in self.rules:
            rule.apply(render_matrix, delta_time, self.vector_processor)
