param([switch]$Console)
$noconsole = "--disable-console"
if ($Console.IsPresent) {
    $noconsole = ""
}
stop-process -ProcessName pyau*
python -m nuitka --output-dir=.build $noconsole --include-package=pyclip,requests,dotenv --standalone --onefile pyautokey.py
