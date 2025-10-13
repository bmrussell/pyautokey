import time
from dataclasses import dataclass
from typing import Optional

import pyautogui
import win32gui
from pynput.keyboard import HotKey

import factory

WINDOW_CLASS = 'CabinetWClass'  # Window class for Windows Explorer

def is_file_explorer_active():
    hwnd = win32gui.GetForegroundWindow()
    return win32gui.GetClassName(hwnd) == WINDOW_CLASS

@dataclass
class NavPane:

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
        
    def invoke(self)->Optional[str]:

        if is_file_explorer_active():
            for key_in_sequence in self.shortmatch_arr:            
                key_in_sequence.release()            

            pyautogui.PAUSE = 0           # Default is 0.1 seconds between actions
            pyautogui.MINIMUM_DURATION = 0# Optional: no minimum hold time for keypresses
            pyautogui.MINIMUM_SLEEP = 0   # Optional: disable small sleep between actions
            pyautogui.FAILSAFE = False    # Optional: disables moving mouse to corner to stop script
                              #
            pyautogui.hotkey('ctrl', 'f')
            pyautogui.press(['tab', 'tab', 'left', 'left', 'enter'])
            time.sleep(0.1)
            pyautogui.press(['up', 'enter', 'enter'])
            
            time.sleep(0.1)
            pyautogui.press('enter')

            time.sleep(0.1)
            pyautogui.press(['tab', 'tab', 'tab'])
       
        return None
    
def register() -> None:
    factory.register("plug_navpane", NavPane)
