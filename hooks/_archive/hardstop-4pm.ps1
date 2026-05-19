# hardstop-4pm.ps1
# Fires on every Stop event. Checks if it's past 4pm CT.
# Outputs a warning to stdout so Claude sees it.

$raw = [Console]::In.ReadToEnd()

# Get current Central Time
$ct = [System.TimeZoneInfo]::ConvertTimeBySystemTimeZone((Get-Date), "Central Standard Time")
$hour = $ct.Hour

if ($hour -ge 16) {
    Write-Output "HARD STOP WARNING: It is $($ct.ToString('h:mm tt')) CT. Time to get home to Chloe and Silas. Wrap up NOW."
} elseif ($hour -ge 15 -and $ct.Minute -ge 30) {
    Write-Output "HEADS UP: It is $($ct.ToString('h:mm tt')) CT. 30 minutes until hard stop. Start wrapping up."
}
