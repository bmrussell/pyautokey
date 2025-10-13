from typing import Optional, Protocol


class Plugin(Protocol):
    """Basic protocol interface"""
    
    def invoke(self) -> Optional[str]:
        pass