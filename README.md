# PYAUTOKEY

Small project to replace the functions I commonly use Autohotkey for. The end goal may be to incorporate loading and running python modules on the fly, opening up massive flexibility without the baggage of Autohotkey scripting syntax (no shade, I've used it for years).

---
# CURRENT FEATURES

- Static text replacement.
- System tray icon. Right click and choose Quit to exit.

## CONFIGURATION FILE
JSON configuration file `pyautokey.json` in the current directory or `%APPDATA%\pyautokey`. File should be UTF-8 encoded. Contents as follows:

### SECTION `config`
|Key|Value|
|--|--|
|`macro_start`|Character that will start looking for a text expansion. I use `:`
|`macro_end`|Character that will trigger text expansion. I use space. This is defined in the config here as "Key.space" which translates directly to `pynput` hotkey parsing.

### SECTION `replacements`
Multiple key, value entries of text to watch for and text it will be replaced with. Special characters that `pynput` recognises are surrounded by `<` `>` so `<enter>` for the enter key.

---
# BUILD
```powershell
pyinstaller --hidden-import pkg_resources --hidden-import infi.systray --onefile --noconsole .\pyautokey.py
```

---
# REFERENCES
