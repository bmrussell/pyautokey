import json
import os
import re
import sys
import time

import icoextract
import pyautogui
import pyperclip
from infi.systray import SysTrayIcon
from pynput import keyboard

import factory
import loader

special_chars_to_be_typed = {
    "<tab>": "\t"
    ,"<enter>": "\n"
    ,"<space>":" "
    }

def quit(tray):
    global quit_selected
    global listener

    quit_selected = True
    listener.stop()


def on_press(key):
    global typed_keys
    global listening
    global actions

    key_str = str(key).replace('\'', '')

    if key_str == macro_start:
        typed_keys = []
        listening = True
        

    if listening:
        if key_str == macro_end:
            #print(f'key_str=[{key_str}] is space == {key_str == " "}')
            candidate_keyword = ''.join(typed_keys)[1:]
            #print(f'candidate_keyword={candidate_keyword}.')
            if candidate_keyword != "":
                if candidate_keyword in replacements.keys():
                    listening = False                             
                    pyautogui.press('backspace', presses=len(candidate_keyword)+2)
                    for fragment in replacements[candidate_keyword]:
                        action = None
                        special = None
                        delay = None
                        try:
                            if fragment[0] == '<':
                                special = keyboard.HotKey.parse(fragment)
                        except:
                            # Was a <name> but not a hotkey
                            if fragment in actions:
                                # is a plugin
                                action = actions[fragment]
                            elif len(fragment) > 7 and fragment[:7] == '<delay ':
                                # Is a delay
                                delay = float(fragment[7:][:-1])/1000

                        # print(f'fragment={fragment}, action={action}, special={special}')
                        if action != None:
                            # This is text replacement so
                            # Create an instance of the action for the right plugin
                            # And call it to get the replacement text type it
                            plugin = factory.create(action)
                            expansion = plugin.invoke()
                            pyautogui.typewrite(expansion)
                            # pyperclip.copy(expansion)
                            # pyautogui.hotkey("ctrl", "v")
                            # print(fragment, end='')
                        elif delay != None:
                            time.sleep(delay)
                        elif fragment in special_chars_to_be_typed:
                            pyautogui.typewrite(special_chars_to_be_typed[fragment])
                        elif special == None:
                            # Clipboard is a work-around for
                            # pyautogui.typewrite not dealing with extended characters
                            oldClipboard = pyperclip.paste()
                            pyperclip.copy(fragment)
                            pyautogui.hotkey("ctrl", "v")
                            pyperclip.copy(oldClipboard)
                            # print(fragment, end='')
                        else:
                            pyautogui.hotkey(special)
                            # print(f'[{special}]', end='')

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


if __name__ == '__main__':
    global systray
    global quit_selected
    global listener
    global actions

    # Initialise
    datadir = os.path.join(os.getenv('APPDATA'), 'pyautokey')

    if not os.path.exists(datadir):
        os.makedirs(datadir)

    # Get the app icon from Windows
    extractor = icoextract.IconExtractor('C:\\Windows\\SystemResources\\imageres.dll.mun')
    iconfile = f'{datadir}\\pyautokey.ico'
    extractor.export_icon(iconfile, 173)

    # Initialise system tray
    systray = SysTrayIcon(iconfile, "...", menu_options=[], on_quit=quit)
    systray.start()
    

    appdata_config = os.path.join(datadir, 'pyautokey.json')
    if os.path.exists('pyautokey.json'):
        config_file = 'pyautokey.json'
    elif os.path.exists(appdata_config):
        config_file = appdata_config

    # Read the config
    try:
        
        print(f'cwd = {os.getcwd()}')
        print(f'Loading config from {config_file}...', end='')
        with open(config_file, 'r', encoding='utf-8') as json_file:
            config_json = json.load(json_file)
        print('Done')
    except:
        print("Could not open config file.")
        sys.exit(0)

    # Load text replacements
    macro_start = config_json['config']['macro_start']
    macro_end = config_json['config']['macro_end']
    replacements = config_json['replacements']
    prep_replacements(replacements)

    # Load Plugins
    print(f"Loading plugins: {config_json['plugins']}")
    loader.load_plugins(config_json['plugins'])

    # Load the actions into a dictionary indexed on shortmatch
    # that do something with those plugins
    actions = {item["shortmatch"]: item for item in config_json["actions"] if item['trigger'] == 'replacement'}
        
    # Handle Hotkeys
    # Create a dictionary of keys/functions for pynput
    hotkey_listener = None
    listen_for = {}    
    for key, hotkey in {item["shortmatch"]: item for item in config_json["actions"] if item['trigger'] == 'hotkey'}.items():
        plugin = factory.create(hotkey)
        listen_for[key] = plugin.invoke
        
    if len(listen_for) > 0:
        hotkey_listener = keyboard.GlobalHotKeys(listen_for)
        hotkey_listener.start()    

    # Load the asynchronous plugins that we'll call with asyncio.
    for key, hotkey in {item["shortmatch"]: item for item in config_json["actions"] if item['trigger'] == 'async'}.items():
        plugin = factory.create(hotkey)        
        plugin.invoke()

    # Start the text expansion listener: blocking.
    listening = True
    typed_keys = []
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    
    # Cleanup
    if hotkey_listener != None:
        hotkey_listener.stop()
        
    systray.shutdown()
    sys.exit(0)

