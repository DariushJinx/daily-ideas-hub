param(
    [string]$Title = "ایده‌های روزانه کسب‌وکار",
    [string]$Message = "سیستم نوتیفیکیشن ویندوز فعال شد! هر روز ساعت ۱۳ منتظر ایده‌های جدید باشید."
)

[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
[Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null

$xmlTemplate = @"
<toast>
    <visual>
        <binding template="ToastGeneric">
            <text>$Title</text>
            <text>$Message</text>
        </binding>
    </visual>
</toast>
"@

$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($xmlTemplate)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("DailyIdeasHub").Show($toast)
Write-Output "Toast notification sent successfully!"
