@echo off
setlocal

set ALIAS=doskey markdown=python -m mrkdwn.main $*

rem Determine the shell config file
set "USERPROFILE=%USERPROFILE%"
set "CMD_CONFIG=%USERPROFILE%\cmd_aliases.bat"
set "POWERSHELL_PROFILE=%USERPROFILE%\Documents\WindowsPowerShell\Microsoft.PowerShell_profile.ps1"

if exist "%CMD_CONFIG%" (
    echo File %CMD_CONFIG% exists.
) else (
    echo Creating %CMD_CONFIG%.
    echo @echo off > "%CMD_CONFIG%"
)

if exist "%POWERSHELL_PROFILE%" (
    echo File %POWERSHELL_PROFILE% exists.
) else (
    echo Creating %POWERSHELL_PROFILE%.
    echo # PowerShell profile > "%POWERSHELL_PROFILE%"
)

rem Add the alias if it doesn't exist
findstr /c:"%ALIAS%" "%CMD_CONFIG%" >nul
if %errorlevel% neq 0 (
    echo %ALIAS% >> "%CMD_CONFIG%"
    echo Alias added to %CMD_CONFIG%. Please restart your terminal or run the following command: call %CMD_CONFIG%
) else (
    echo Alias already exists in %CMD_CONFIG%.
)

rem Add to PowerShell profile
findstr /c:"%ALIAS%" "%POWERSHELL_PROFILE%" >nul
if %errorlevel% neq 0 (
    echo doskey markdown=python -m mrkdwn.main $* >> "%POWERSHELL_PROFILE%"
    echo Alias added to %POWERSHELL_PROFILE%. Please restart your terminal or run the following command: . "%POWERSHELL_PROFILE%"
) else (
    echo Alias already exists in %POWERSHELL_PROFILE%.
)

endlocal
