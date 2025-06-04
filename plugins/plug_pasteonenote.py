import time
from dataclasses import dataclass

import pyautogui
import pyclip
from pynput import keyboard
from pynput.keyboard import Controller, HotKey, Key

import factory


@dataclass
class PasteTitle:

    trigger: str
    shortmatch: str
    shortmatch_arr = []

    def __init__(self, trigger, shortmatch):
        # Optimisation
        #   Key the pynput keycodes for control keys in this
        #   hotkey sequence for use when invoked
        this_sequence = shortmatch.split('+')
        shortmatch_arr = []
        for key_s in this_sequence:
            try:
                shortmatch_arr.append(HotKey.parse(key_s))                
            except:
                pass 
        
    def invoke(self)->str:        
        # Make sure the hotkeys are released
        for key_in_sequence in self.shortmatch_arr:
            keyboard.release(key_in_sequence)
        
        # Copy, trim then paste           
        clipboard_text = pyclip.paste().decode('UTF-8')
        url = clipboard_text.split('\n')
        if len(url) == 2 and url[1].startswith("onenote:"):
            pyautogui.PAUSE = 0.1
            pyclip.copy(url[1])
            pyautogui.keyDown("ctrl")
            time.sleep(0.05)
            pyautogui.press("v")
            time.sleep(0.05)
            pyautogui.keyUp("ctrl")        
        return None
    
def register() -> None:
    factory.register("plug_pasteonenote", PasteTitle)
