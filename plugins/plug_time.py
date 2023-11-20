import datetime
from dataclasses import dataclass

from pluginframework import factory


@dataclass
class PluginTime:
     
    trigger: str
    shortmatch: str

    def invoke(self)->str:
        return datetime.datetime.now().strftime('%H:%M')
    
def register() -> None:
    factory.register("plug_time", PluginTime)
