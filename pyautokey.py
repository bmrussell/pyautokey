import json
import os
import re

import pyautogui
from pynput import keyboard
from pynput.keyboard import Key, Listener

hotkeys = ['\t', '\n', '\r', 
           'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
           'browserback', 'browserfavorites', 'browserforward', 'browserhome',
           'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
           'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
           'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
           'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
           'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
           'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
           'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
           'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
           'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
           'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
           'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
           'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
           'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
           'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
           'command', 'option', 'optionleft', 'optionright']


def on_press(key):
    global typed_keys
    global listening

    key_str = str(key).replace('\'', '')

    if key_str == macro_start:
        typed_keys = []
        listening = True

    if listening:
        if key_str == macro_end:
            print(f'key_str=[{key_str}] is space == {key_str == " "}')
            candidate_keyword = ''.join(typed_keys)[1:]
            print(f'candidate_keyword={candidate_keyword}.')
            if candidate_keyword != "":
                if candidate_keyword in replacements.keys():
                    listening = False
                    pyautogui.press('backspace', presses=len(candidate_keyword)+2)
                    for fragment in replacements[candidate_keyword]:
                        try:
                            special = keyboard.HotKey.parse(fragment)
                            special = fragment[1:-1]
                        except:
                            special = None
                            
                        if special == None:
                            pyautogui.typewrite(fragment)
                            print(fragment, end='')
                        else:
                            pyautogui.hotkey(special)
                            print(f'[{special}]', end='')
                            
        else:
            typed_keys.append(key_str)


def prep_replacements(replacements):
    """Parse all the replacement strings
    Replace the replacement string with an array containing entries that are special character placeholders like <enter> with their Key enum equivalent
    e.g. Key.enter or sequences of regular characters
    """
    # keyboard.HotKey.parse('<enter>') 
    pattern = re.compile(r'(<[^>]+>|[^<]+)')
    for key, value in replacements.items():
        matches = pattern.findall(value)
        replacement_array = []
        for match in matches:
            if match[0] == '<' and match[-1] == '>':
                try:
                    # If it's a hotkey make sure its transformed to lower case
                    # for use in pyautogui.hotkey() on expansion
                    hotkey = keyboard.HotKey.parse(match.lower())
                    replacement_array.append(match.lower())
                except:
                    # It wasn't a hotkey, just something like <blARble>
                    replacement_array.append(match)
            else:
                replacement_array.append(match)
            
            replacements[key] = replacement_array
    

appdata_config = os.path.join(
    os.getenv('APPDATA'), 'pyautokey', 'pyautokey.json')
if os.path.exists('pyautokey.json'):
    config_file = 'pyautokey.json'
elif os.path.exists(appdata_config):
    config_file = appdata_config


with open(config_file) as json_file:
    config_json = json.load(json_file)

macro_start = config_json['config']['macro_start']
macro_end = config_json['config']['macro_end']
replacements = config_json['replacements']
prep_replacements(replacements)

listening = True
typed_keys = []

with Listener(on_press=on_press) as listener:
    listener.join()

pass
