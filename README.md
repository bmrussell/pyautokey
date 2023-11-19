# PYAUTOKEY

Small project to replace the functions I commonly use Autohotkey for. The end goal may be to incorporate loading and running python modules on the fly, opening up massive flexibility without the baggage of Autohotkey scripting syntax (no shade, I've used it for years).

---
# CURRENT FEATURES

- Static text replacement.
- System tray icon. Right click and choose Quit to exit.

## CONFIGURATION FILE
JSON configuration file `pyautokey.json` in the current directory or `%APPDATA%\pyautokey`. File should be UTF-8 encoded. Contents as follows:

The application implement a plugin architecture by placing python modules in a `plugins` directory. The module should implement a `@dataclass` which has an `invoke()` method and the module should contain a `register()` method which calls `factory.register("module_name", class_name)`. See the included examples for more information.

### SECTION `config`
|Key|Value|
|--|--|
|`macro_start`|Character that will start looking for a text expansion. I use `:`
|`macro_end`|Character that will trigger text expansion. I use space. This is defined in the config here as "Key.space" which translates directly to `pynput` hotkey parsing.
|`plugins`|Defines names of plugin classes to load from the `plugins`` directory. Values should be `plugins.` followed by the name of the Python file with no extension|
|`actions`|Defines actions which will be executed by plugins. See below for action specification|

#### ACTION SPECIFICATION
Actions are described key/value pairs as follows:
|Key|Value|
|--|--|
|`type`|The type of plugin that will execute this action|
|`trigger`|When the action is invoked. Currently `replacement` for use during text expansion or `hotkey` for hotkeys.|
|`match`|Used to determine when the trigger applies. Either the text that will act as the signal to call the plugin, obtain the text and use it for expansion, or the hotkey to wait on that will invoke the plugin|

### SECTION `replacements`
Multiple key, value entries of text to watch for and text it will be replaced with. Special characters that `pynput` recognises are surrounded by `<` `>` so `<enter>` for the enter key.

---
# BUILD
```powershell
pyinstaller --hidden-import pkg_resources --hidden-import infi.systray --onefile --noconsole .\pyautokey.py
```

---
# REFERENCES
* [The Power Of The Plugin Architecture In Python](https://www.youtube.com/watch?v=iCE1bDoit9Q)