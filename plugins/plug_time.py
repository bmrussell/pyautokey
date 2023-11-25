import datetime
from dataclasses import dataclass

import factory


@dataclass
class PluginTime:

    def invoke(self)->str:
        return datetime.datetime.now().strftime('%H:%M')
    
def register() -> None:
    factory.register("plug_time", PluginTime)
