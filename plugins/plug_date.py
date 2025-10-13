import datetime
from dataclasses import dataclass
from typing import Optional

import factory


@dataclass
class PluginDate:
     
    trigger: str
    shortmatch: str

    def invoke(self)->Optional[str]:
        return datetime.datetime.now().strftime('%d/%m/%Y')
    
def register() -> None:
    factory.register("plug_date", PluginDate)
