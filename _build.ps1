param([switch]$Console)
$noconsole = "--disable-console"
if ($Console.IsPresent) {
    $noconsole = ""
}
python -m nuitka --output-dir=.build $noconsole --include-package=pyclip,requests,dotenv --standalone --onefile pyautokey.py


# Directory
#python -m nuitka --output-dir=.build --onefile .\pyautokey.py
