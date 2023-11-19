from typing import Protocol


class Plugin(Protocol):
    """Basic protocol interface"""
    
    def invoke(self) -> str:
        pass