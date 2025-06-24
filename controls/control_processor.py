from typing import List
from .base_controls import BaseControls

class ControlProcessor:
    """Manages and delegates to multiple control schemes"""
    
    def __init__(self):
        self.controls: List[BaseControls] = []
    
    def register_control(self, control: BaseControls):
        """Add a new control scheme to be processed"""
        self.controls.append(control)
    
    def handle_event(self, event):
        """Delegate event to all registered controls"""
        for control in self.controls:
            control.handle_event(event)
    
    def update(self):
        """Update all registered controls"""
        for control in self.controls:
            control.update()
