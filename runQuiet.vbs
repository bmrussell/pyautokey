cmd = ""
parameterName = ""
waitms = 0
For each arg in WScript.Arguments

	If parameterName <> "" Then
		If parameterName = "~WAIT" Then		' Use ~ to avoid conflict with program being launchged
			waitms = CInt(arg) * 1000
		End If
		parameterName = ""
	Else
		' Have a switch		
		if Left(arg, 1) = "~" Then
			' arg indicates what we are to read from the argument list next
			' So set parameterName to this
			parameterName = UCase(arg)
		Else			
			if cmd <> "" Then
				cmd = cmd & " "
			End If 
			argStr = """" & arg & """"
			cmd = cmd & argStr
		End If
	End If
Next

If waitms > 0 Then
	WScript.Sleep waitms
End If
CreateObject("Wscript.Shell").Run cmd, 0, False

'pwsh.exe ~WindowStyle Hidden ~File "C:\Users\brussell4\OneDrive ~ DXC Production\Code\Powershell\Cal~GetFreeBusy.ps1" ~SaveAs o:\dxc.com\brussell4.html ~Silent

'"runQuiet.vbs" pwsh.exe ~WindowStyle Hidden ~File "C:\Users\brussell4\OneDrive ~ DXC Production\Code\Powershell\Cal~GetFreeBusy.ps1" ~SaveAs o:\dxc.com\brussell4.html ~Silent

' https://docs.microsoft.com/en~us/office/vba/language/reference/user~interface~help/ucase~function