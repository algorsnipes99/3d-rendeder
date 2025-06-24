from abc import ABC, abstractmethod

class BaseControls(ABC):
    """Abstract base class for all control schemes"""
    
    @abstractmethod
    def handle_event(self, event):
        """Handle pygame event"""
        pass

    @abstractmethod
    def update(self):
        """Perform any per-frame updates"""
        pass
