from typing import Optional, Protocol


class Plugin(Protocol):
    """Basic protocol interface"""
    
    def invoke(self, **kwargs) -> Optional[str]:
        pass