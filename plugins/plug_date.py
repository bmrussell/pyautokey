import datetime
from dataclasses import dataclass

from pluginframework import factory


@dataclass
class PluginDate:
     
    trigger: str
    shortmatch: str

    def invoke(self)->str:
        return datetime.datetime.now().strftime('%d/%m/%Y')
    
def register() -> None:
    factory.register("plug_date", PluginDate)
