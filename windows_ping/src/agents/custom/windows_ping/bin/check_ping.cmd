@echo off
REM Kuhn & Rueß GmbH
REM Wrapper for check_ping.ps1 so the Checkmk Windows agent can invoke the
REM ping check via MRPE with a short, sane command line. Resolves
REM powershell.exe via %SystemRoot%, points -File at the .ps1 sitting next
REM to this wrapper (%~dp0), forwards all arguments and preserves the
REM Nagios exit code emitted by the script.
"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -NoLogo -ExecutionPolicy Bypass -File "%~dp0check_ping.ps1" %*
exit /b %ERRORLEVEL%
