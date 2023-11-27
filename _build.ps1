# One file
#python -m nuitka --disable-console --output-dir=.build --onefile-tempdir-spec=C:\ProgramData\pyautokey --onefile .\pyautokey.py
python -m nuitka --disable-console --output-dir=.build --standalone --onefile pyautokey.py

# Directory
#python -m nuitka --output-dir=.build --onefile .\pyautokey.py
