import time
from dataclasses import dataclass
from typing import Optional

import keyboard
import pygetwindow as gw
import pyperclip
from pynput.keyboard import Controller, HotKey, Key

import factory


def safe_write(text, delay=0.02):
    original_window = gw.getActiveWindow()
    print(f"Typing started in: {original_window}")
    
    for ch in text:
        current_window = gw.getActiveWindow()
        if current_window != original_window:
            print(f"Window changed to '{current_window}' — typing stopped.")
            break
        
        keyboard.write(ch, delay=0)
        time.sleep(delay)  # simulate natural typing speed

@dataclass
class TypeInto:

    trigger: str
    shortmatch: str
    shortmatch_arr = []

    def __init__(self, trigger, shortmatch):
        pass
        
    def invoke(self, sysTrayIcon)->Optional[str]:
        time.sleep(0.5)  # Let the menu interaction finish
        initial_window = gw.getActiveWindow()
        print("Monitoring for window change...")
        while True:
            time.sleep(0.1)
            current_window = gw.getActiveWindow()
            if current_window != initial_window:
                print(f"Window changed to: {current_window}")
                time.sleep(2)  # Let the window activate
                print("Pasting...")
                text = pyperclip.paste()
                #keyboard.write(text, delay=0.05)  # type with a slight delay
                safe_write(text, delay=0.06)
                break        
        
        return None
    
def register() -> None:
    factory.register("plug_typeinto", TypeInto)
