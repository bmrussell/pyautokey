import importlib
import importlib.util
import os


class PluginInterface:
    
    @staticmethod
    def register() -> None:
        """Plugin initilisation here in the implementation."""
    
def import_module(name: str) -> PluginInterface:
    original = True
    if original:
        imported_module = importlib.import_module(name) # type: ignore
        return imported_module
    else:    
        s = name.split('.')
        spec = importlib.util.spec_from_file_location(name, os.path.join(os.getcwd(), os.path.join(f"{s[0]}",f"{s[1]}.py")))
        imported_module = importlib.util.module_from_spec(spec)
        return imported_module

def load_plugins(plugins: list[str]) -> None:
    """Load the plugins defined in the list and call their register() function.
       Their register function calls the factory with details on how to create them.
    """
    for plugin_name in plugins:
        print(f"Loading {plugin_name}...", end='')
        plugin = import_module(plugin_name)
        plugin.register()
        print('done.')
    