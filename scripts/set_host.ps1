# Add "<ip> <hostname>" lines to the Windows hosts file (skips names that already exist).
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File scripts\set_host.ps1 -HostName s99.school.vnedu.vn[,s19.school.vnedu.vn]
# Writing the real hosts file needs admin rights: the script asks for them (UAC prompt).
# Exit codes: 0 = all names present with the requested IP, 1 = error / UAC refused, 2 = a name exists with another IP.
param(
    [Parameter(Mandatory = $true)][string[]]$HostName,
    [string]$Ip = '10.159.21.68',
    [string]$HostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"
)
$ErrorActionPreference = 'Stop'

# With -File, "a,b" arrives as one string.
$names = @($HostName | ForEach-Object { $_ -split ',' } | ForEach-Object { $_.Trim().ToLower() } | Where-Object { $_ } | Select-Object -Unique)
foreach ($n in $names) {
    if ($n -notmatch '^([a-z0-9]([a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$') {
        Write-Output "INVALID hostname (no http://, no path): $n"; exit 1
    }
}
$parsed = $null
if (-not [System.Net.IPAddress]::TryParse($Ip, [ref]$parsed)) { Write-Output "INVALID IP: $Ip"; exit 1 }

function Get-HostIp([string]$Name) {
    foreach ($line in Get-Content -LiteralPath $HostsPath) {
        $parts = @(($line -replace '#.*', '').Trim() -split '\s+')
        if ($parts.Count -gt 1 -and ($parts[1..($parts.Count - 1)] -contains $Name)) { return $parts[0] }
    }
}

$missing = @(); $conflict = $false
foreach ($n in $names) {
    $current = Get-HostIp $n
    if (-not $current) { $missing += $n }
    elseif ($current -eq $Ip) { Write-Output "EXISTS: $current $n" }
    else { Write-Output "CONFLICT (not changed): $n already points to $current"; $conflict = $true }
}

if ($missing.Count -gt 0) {
    $realHosts = $HostsPath -eq "$env:SystemRoot\System32\drivers\etc\hosts"
    $isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    if ($realHosts -and -not $isAdmin) {
        $argLine = "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -HostName $($missing -join ',') -Ip $Ip"
        try { Start-Process powershell.exe -Verb RunAs -Wait -WindowStyle Hidden -ArgumentList $argLine }
        catch { Write-Output "FAILED: admin permission refused."; exit 1 }
    }
    else {
        $text = [IO.File]::ReadAllText($HostsPath)
        $add = ''
        if ($text.Length -gt 0 -and -not $text.EndsWith("`n")) { $add = "`r`n" }
        foreach ($n in $missing) { $add += "$Ip`t$n`r`n" }
        [IO.File]::AppendAllText($HostsPath, $add, [Text.Encoding]::ASCII)
        if ($realHosts) { Clear-DnsClientCache }
    }
    foreach ($n in $missing) {
        if ((Get-HostIp $n) -eq $Ip) { Write-Output "ADDED: $Ip $n" }
        else { Write-Output "FAILED: could not add $n"; exit 1 }
    }
}
if ($conflict) { exit 2 }
exit 0
