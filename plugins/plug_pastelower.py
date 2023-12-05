import time
from dataclasses import dataclass

import pyautogui
import pyclip
from pynput import keyboard
from pynput.keyboard import Controller, HotKey, Key

import factory


@dataclass
class PasteLower:

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
        
        # Copy, uppercase then paste
        pyautogui.hotkey('ctrl', 'c')        
        clipboard_text = pyclip.paste().decode('UTF-8')        
        upper_text = clipboard_text.lower()        
        pyclip.copy(upper_text)
        pyautogui.hotkey('ctrl', 'v')
                
        # print(f'{self.shortmatch}: clipboard_text={clipboard_text} --> {upper_text}')
        return None
    
def register() -> None:
    factory.register("plug_pastelower", PasteLower)
