Set WshShell = CreateObject("WScript.Shell") 

strPath = Wscript.ScriptFullName
Set fso = CreateObject("Scripting.FileSystemObject")
Set objFile = fso.GetFile(strPath)
strFolder = fso.GetParentFolderName(objFile)

app_logger_full_path = fso.BuildPath(strFolder, "start_ap_logger.bat")

'Wscript.Echo app_logger_full_path

WshShell.Run chr(34) & app_logger_full_path & Chr(34), 0
Set WshShell = Nothing