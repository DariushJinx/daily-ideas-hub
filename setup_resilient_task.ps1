$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "C:\Users\salimi\.gemini\antigravity\scratch\daily-ideas-hub\run_daily_silent.vbs"
$trigger = New-ScheduledTaskTrigger -Daily -At "13:00"
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -WakeToRun
Register-ScheduledTask -TaskName "DailyBusinessIdeas" -Action $action -Trigger $trigger -Settings $settings -Force
Write-Host "SUCCESS: Task DailyBusinessIdeas registered with StartWhenAvailable and Battery allowances!"
