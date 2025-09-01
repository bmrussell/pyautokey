import asyncio
import logging
import os
import re
import threading
import time
from dataclasses import dataclass

import pyautogui
import pyclip
import win32con
import win32gui
from pynput import keyboard
from pynput.keyboard import Controller, HotKey, Key

import factory


async def watch_for_window(windowtitle: str):
    """
    Monitors for specific windows, removes their title bars, and maximizes them.
    """
    # Regex to match the window title, equivalent to AHK's "Win11-VM|RDP Work"
    title_regex = re.compile(windowtitle)
    logging.debug("Starting Borderless Maximise watcher...")
    while True:
        try:
            hwnd = None
            # Loop until we find an active window that matches the regex
            while not hwnd:
                # Get the handle of the currently active (foreground) window
                active_hwnd = win32gui.GetForegroundWindow()
                if active_hwnd:
                    window_title = win32gui.GetWindowText(active_hwnd)
                    if title_regex.search(window_title):
                        hwnd = active_hwnd
                # Wait a moment before checking again to avoid high CPU usage
                if not hwnd:
                    time.sleep(1)

            # A short delay, similar to the original script
            time.sleep(2)

            # Ensure the window handle is still valid before proceeding
            if not win32gui.IsWindow(hwnd):
                # print("Window closed before modifications could be applied. Restarting search.")
                continue


            # Get the current window style
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)

            if style & win32con.WS_CAPTION:  # only modify if caption bit is set
                # Remove the WS_CAPTION style (which includes the title bar)
                # This is the equivalent of WinSetStyle "-0xC00000"
                new_style = style & ~win32con.WS_CAPTION

                # Apply the new style to the window
                win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, new_style)

                # Maximize the window
                win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

        except Exception as e:
            # The pywin32 functions can raise an exception if the window is destroyed
            # unexpectedly. We catch it and continue the loop.
            time.sleep(2)

_loop = None

# def fire_and_forget():
#     logging.basicConfig(level=logging.DEBUG)
#     loop = asyncio.get_event_loop()
#     loop.set_debug(True)
#     loop.create_task(watch_for_window())
    
def _start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def start_background_loop():
    global _loop
    _loop = asyncio.new_event_loop()
    t = threading.Thread(target=_start_loop, args=(_loop,), daemon=True)
    t.start()

def fire_and_forget(coro):
    asyncio.run_coroutine_threadsafe(coro, _loop) # pyright: ignore[reportArgumentType]
    
@dataclass
class BorderlessMaximise:

    trigger: str
    shortmatch: str
    windowtitle: str

    def __init__(self, trigger, windowtitle):
        # Optimisation
        #   Key the pynput keycodes for control keys in this
        #   hotkey sequence for use when invoked
        self.windowtitle = windowtitle
        
    def invoke(self)->str:
        start_background_loop()
        fire_and_forget(watch_for_window(self.windowtitle))        
        return None
    
def register() -> None:
    factory.register("plug_borderlessmaximise", BorderlessMaximise)
