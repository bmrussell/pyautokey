pyinstaller --onefile --noconsole --clean  `
  --add-data "plugins;plugins"  `
  --collect-all soundfile  `
  --collect-all winsdk  `
  --collect-all dotenv  `
  --collect-all pycaw  `
  --collect-all requests `
  --collect-all pyclip `
  --collect-all win32gui `
  --hidden-import pycaw  `
  --hidden-import winsdk  `
  --hidden-import infi.systray  `
  --hidden-import soundfile  `
  --hidden-import keyboard._winkeyboard  `
  --hidden-import pynput.keyboard  `
  --hidden-import pynput.mouse  `
  --hidden-import MouseInfo `
  --hidden-import winsdk.windows.edia.control  `
  --hidden-import winsdk.windows.media  `
  pyautokey.py