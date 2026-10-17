Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\salimi\.gemini\antigravity\scratch\daily-ideas-hub"
WshShell.Run "python telegram_listener.py", 0, False
