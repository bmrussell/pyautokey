Set oShell = WScript.CreateObject ("WScript.Shell")
oShell.run "cmd.exe /c _run.cmd", 0, False
Set oShell = Nothing