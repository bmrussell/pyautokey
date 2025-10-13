import datetime
from dataclasses import dataclass
from typing import Optional

import factory


@dataclass
class PluginTime:

    trigger: str
    shortmatch: str

    def invoke(self)->Optional[str]:
        return datetime.datetime.now().strftime('%H:%M')
    
def register() -> None:
    factory.register("plug_time", PluginTime)
