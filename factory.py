from typing import Any, Callable

from plugin import Plugin

registered_plugins: dict[str, Callable[..., Plugin]] = {}

def register(plugin_type: str, trigger_func:Callable[..., Plugin]):
    """Register a plugin"""
    registered_plugins[plugin_type] = trigger_func
    
def unregister(plugin_type: str):
    """Unregister a plugin"""
    registered_plugins.pop(plugin_type, None)
    
def create(arguments: dict[str, Any]) -> Plugin:
    """Create an instance of a plugin"""
    args_copy = arguments.copy()
    plugin_type = args_copy.pop('type')
    try:
        invocation_func = registered_plugins[plugin_type]
        return invocation_func(**args_copy)
    except KeyError:
        raise ValueError(f"Unknown plugin type {plugin_type!r}") from None