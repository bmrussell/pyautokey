import datetime
from dataclasses import dataclass
from typing import Optional

import factory


@dataclass
class PluginDate:
     
    trigger: str
    shortmatch: str

    def invoke(self, **kwargs)->Optional[str]:
        expansion = datetime.datetime.now().strftime('%d/%m/%Y')
        
        if kwargs is not None:
             for key, value in kwargs.items():
                 if "shortmatch" in value and value["shortmatch"] == "<idate>":
                     # ISO date
                    expansion = datetime.datetime.now().strftime('%Y-%m-%d')
        
        return expansion
    
def register() -> None:
    factory.register("plug_date", PluginDate)
