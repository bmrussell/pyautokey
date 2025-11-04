# https://stackoverflow.com/questions/37278647/fire-and-forget-python-async-await

import datetime
import os.path
import threading
import time
from dataclasses import dataclass
from typing import Optional

import factory

watchingFor = None

def fire_and_forget(f):
    def wrapped(*args, **kwargs):
        threading.Thread(target=f, args=args, kwargs=kwargs).start()
    return wrapped
    
@dataclass
class PluginUatu:

    trigger: str
    shortmatch: str

    def __init__(self, trigger, shortmatch):        
        global watchingFor
        watchingFor = shortmatch
        print(f"Watching for {watchingFor}")
        pass
    
    @fire_and_forget
    def invoke(self, **kwargs)->Optional[str]:
        while True:
            while watchingFor is not None and not os.path.exists(watchingFor):
                time.sleep(10)
            if watchingFor is not None and os.path.isfile(watchingFor):
                os.remove(watchingFor)
                
def register() -> None:
    factory.register("plug_uatu", PluginUatu)
