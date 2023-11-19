import importlib


class PluginInterface:
    
    @staticmethod
    def register() -> None:
        """Plugin initilisation here in the implementation."""
    
def import_module(name: str) -> PluginInterface:
    return importlib.import_module(name) # type: ignore

def load_plugins(plugins: list[str]) -> None:
    """Load the plugins defined in the list and call their register() function.
       Their register function calls the factory with details on how to create them.
    """
    for plugin_name in plugins:
        plugin = import_module(plugin_name)
        plugin.register()
    